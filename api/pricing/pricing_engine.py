from decimal import Decimal
from typing import List, Dict
from uuid import UUID
import asyncpg

class PricingEngine:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def calculate_configuration_price(self, components: List[Dict]) -> Decimal:
        """
        Calculate the total price of a configuration based on the selected components.
        """
        total_price = Decimal(0)

        async with self.pool.acquire() as conn:
            for component in components:
                component_price = await conn.fetchval(
                    "SELECT base_price FROM components WHERE id = $1",
                    component['id']
                )
                total_price += Decimal(component_price) * Decimal(component.get('quantity', 1))

        return total_price.quantize(Decimal('.01'))

    async def apply_configuration_discounts(self, total_price: Decimal, configuration: Dict) -> Decimal:
        """
        Apply any relevant discounts to the configuration price.
        """
        # Example: 5% discount for carbon frames
        frame_id = configuration['base_component_id']
        frame_material = await self._get_component_material(frame_id)
        if frame_material == 'carbon':
            total_price *= Decimal(0.95)

        return total_price.quantize(Decimal('.01'))

    async def _get_component_material(self, component_id: UUID) -> str:
        """
        Get the material of a given component.
        """
        async with self.pool.acquire() as conn:
            material = await conn.fetchval(
                "SELECT attributes->'material' FROM components WHERE id = $1",
                component_id
            )
            return material or ''