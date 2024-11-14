from typing import List, Dict
from uuid import UUID
import asyncpg
import json
from dataclasses import dataclass

@dataclass
class CompatibilityRule:
    id: UUID
    name: str
    description: str
    rule_type: str
    component_id: UUID
    related_component_id: UUID
    condition_expression: Dict

class RulesEngine:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def validate_configuration(self, configuration: Dict) -> bool:
        """
        Validate a given configuration against all applicable compatibility rules.
        """
        async with self.pool.acquire() as conn:
            # Get all relevant compatibility rules
            rules = await self._get_applicable_rules(conn, configuration)

            for rule in rules:
                if not await self._validate_rule(conn, rule, configuration):
                    return False

        return True

    async def _get_applicable_rules(self, conn: asyncpg.Connection, configuration: Dict) -> List[CompatibilityRule]:
        """
        Retrieve all compatibility rules that apply to the given configuration.
        """
        query = """
            SELECT 
                id, name, description, rule_type, 
                component_id, related_component_id, condition_expression
            FROM compatibility_rules
            WHERE component_id = $1 
               OR related_component_id = ANY($2::uuid[])
        """
        component_ids = [configuration['base_component_id']]
        component_ids.extend(c['id'] for c in configuration['components'])

        rows = await conn.fetch(query, configuration['base_component_id'], component_ids)
        return [CompatibilityRule(**row) for row in rows]

    async def _validate_rule(self, conn: asyncpg.Connection, rule: CompatibilityRule, configuration: Dict) -> bool:
        """
        Validate a single compatibility rule against the given configuration.
        """
        if rule.rule_type == 'REQUIRES':
            return await self._validate_requires_rule(conn, rule, configuration)
        elif rule.rule_type == 'EXCLUDES':
            return await self._validate_excludes_rule(conn, rule, configuration)
        elif rule.rule_type == 'CONDITIONAL':
            return await self._validate_conditional_rule(conn, rule, configuration)
        return True

    async def _validate_requires_rule(self, conn: asyncpg.Connection, rule: CompatibilityRule, configuration: Dict) -> bool:
        """
        Validate a 'REQUIRES' compatibility rule.
        """
        # Check if the required component is present in the configuration
        for component in configuration['components']:
            if component['id'] == rule.related_component_id:
                return True
        return False

    async def _validate_excludes_rule(self, conn: asyncpg.Connection, rule: CompatibilityRule, configuration: Dict) -> bool:
        """
        Validate an 'EXCLUDES' compatibility rule.
        """
        # Check if the excluded component is present in the configuration
        for component in configuration['components']:
            if component['id'] == rule.related_component_id:
                return False
        return True

    async def _validate_conditional_rule(self, conn: asyncpg.Connection, rule: CompatibilityRule, configuration: Dict) -> bool:
        """
        Validate a 'CONDITIONAL' compatibility rule.
        """
        # Decode the condition expression from JSON
        condition = rule.condition_expression

        # Retrieve the attribute values for the components involved in the rule
        frame_attributes = await self._get_component_attributes(conn, configuration['base_component_id'])
        related_component = next((c for c in configuration['components'] if c['id'] == rule.related_component_id), None)
        related_attributes = await self._get_component_attributes(conn, rule.related_component_id) if related_component else {}

        # Evaluate the condition expression
        try:
            if_condition = condition['if']
            then_condition = condition['then']

            if_result = all(frame_attributes.get(k) == v for k, v in if_condition.items())
            then_result = all(related_attributes.get(k) == v for k, v in then_condition.items())

            return if_result and then_result
        except (KeyError, TypeError):
            return False

    async def _get_component_attributes(self, conn: asyncpg.Connection, component_id: UUID) -> Dict:
        """
        Retrieve the attributes of a given component from the database.
        """
        attributes = await conn.fetchval(
            "SELECT attributes FROM components WHERE id = $1",
            component_id
        )
        return json.loads(attributes) if attributes else {}