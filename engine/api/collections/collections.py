import requests
import json
from typing import Dict, Any, Optional
import logging
import time
from pathlib import Path

class StrapiAPIClient:
    def __init__(self, base_url: str, email: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        self._authenticate(email, password)

    def _authenticate(self, email: str, password: str) -> None:
        """Authenticate with Strapi and store JWT token."""
        auth_url = f"{self.base_url}/admin/login"
        response = self.session.post(
            auth_url,
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        token = response.json()["data"]["token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _tokenauthenticate(self) -> None:
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def create_content_type(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new content type in Strapi."""
        url = f"{self.base_url}/content-type-builder/content-types"
        response = self.session.post(url, json=schema)
        response.raise_for_status()
        return response.json()

    def create_component(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new component in Strapi."""
        url = f"{self.base_url}/content-type-builder/components"
        response = self.session.post(url, json=schema)
        response.raise_for_status()
        return response.json()

    def wait_for_build(self, timeout: int = 30) -> None:
        """Wait for Strapi to rebuild after schema changes."""
        time.sleep(timeout)

class ProductConfiguratorSetup:
    def __init__(self, client: StrapiAPIClient):
        self.client = client
        self.schemas_dir = Path("schemas")
        self.components_dir = Path("components")

    def create_shared_components(self) -> None:
        """Create all shared components."""
        components = {
            "shared.price-modifier": {
                "displayName": "PriceModifier",
                "category": "shared",
                "attributes": {
                    "type": {
                        "type": "enumeration",
                        "enum": ["fixed", "percentage", "formula"],
                        "required": True
                    },
                    "value": {"type": "decimal"},
                    "formula": {"type": "text"},
                    "currency": {"type": "string"}
                }
            },
            "shared.inventory": {
                "displayName": "Inventory",
                "category": "shared",
                "attributes": {
                    "sku": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "backorderAllowed": {"type": "boolean", "default": False},
                    "leadTime": {"type": "integer"}
                }
            },
            "rule.conditions": {
                "displayName": "RuleConditions",
                "category": "rule",
                "attributes": {
                    "type": {
                        "type": "enumeration",
                        "enum": ["component", "option", "quantity", "custom"],
                        "required": True
                    },
                    "operator": {
                        "type": "enumeration",
                        "enum": ["equals", "not_equals", "includes", "excludes", "greater_than", "less_than"],
                        "required": True
                    },
                    "value": {"type": "json", "required": True},
                    "customLogic": {"type": "text"}
                }
            }
        }

        for name, schema in components.items():
            try:
                self.client.create_component({
                    "component": {
                        "category": schema["category"],
                        "icon": "cube",
                        "displayName": schema["displayName"],
                        "attributes": schema["attributes"]
                    }
                })
            except Exception as e:
                logging.error(f"Failed to create component {name}: {str(e)}")

    def create_content_types(self) -> None:
        """Create all content types."""
        content_types = {
            "product-family": {
                "singularName": "product-family",
                "pluralName": "product-families",
                "displayName": "Product Family",
                "attributes": {
                    "name": {"type": "string", "required": True},
                    "code": {"type": "string", "required": True, "unique": True},
                    "description": {"type": "text"},
                    "products": {
                        "type": "relation",
                        "relation": "oneToMany",
                        "target": "api::product.product"
                    },
                    "metadata": {"type": "json"}
                }
            },
            # Add other content types here...
        }

        for name, schema in content_types.items():
            try:
                self.client.create_content_type({
                    "contentType": {
                        "displayName": schema["displayName"],
                        "singularName": schema["singularName"],
                        "pluralName": schema["pluralName"],
                        "attributes": schema["attributes"]
                    }
                })
            except Exception as e:
                logging.error(f"Failed to create content type {name}: {str(e)}")

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize client
    client = StrapiAPIClient(
        base_url="http://localhost:1337",
        #email="admin@example.com",
        #password="your_password"
    )
    
    # Initialize setup
    setup = ProductConfiguratorSetup(client)
    
    try:
        # Create components first
        logging.info("Creating shared components...")
        setup.create_shared_components()
        client.wait_for_build()
        
        # Create content types
        logging.info("Creating content types...")
        setup.create_content_types()
        client.wait_for_build()
        
        logging.info("Setup completed successfully!")
        
    except Exception as e:
        logging.error(f"Setup failed: {str(e)}")
        raise

'''
if __name__ == "__main__":
    main()
'''
