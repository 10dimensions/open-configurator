from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import httpx
import pandas as pd
import json
from typing import Dict, List, Optional
from pydantic import BaseModel
import io
import asyncio
import os
from enum import Enum

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Configuration
STRAPI_URL = os.environ["OC_URL"] #"http://localhost:1337"
STRAPI_TOKEN = os.environ["OC_TOKEN"] #"your_token_here"

print(STRAPI_TOKEN)
print(STRAPI_URL)

# Models
class Collection(str, Enum):
    PRODUCT_FAMILIES = "product-families"
    PRODUCTS = "products"
    COMPONENTS = "components"
    OPTIONS = "options"
    RULES = "rules"
    PRICING_RULES = "pricing-rules"
    VISUALIZATIONS = "visualizations"

class Document(BaseModel):
    data: Dict

class BulkResponse(BaseModel):
    success: List[Dict]
    errors: List[Dict]

# Strapi client
class StrapiClient:
    def __init__(self):
        self.base_url = STRAPI_URL
        self.headers = {
            "Authorization": f"Bearer {STRAPI_TOKEN}",
            "Content-Type": "application/json"
        }
        
    async def create_document(self, collection: str, data: Dict) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/{collection}",
                json={"data": data},
                headers=self.headers
            )
            if response.status_code not in (200, 201):
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return response.json()

    async def update_document(self, collection: str, id: int, data: Dict) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/api/{collection}/{id}",
                json={"data": data},
                headers=self.headers
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return response.json()

# CSV processors
class CSVProcessor:
    @staticmethod
    def process_product_families(df: pd.DataFrame) -> List[Dict]:
        return df.apply(lambda row: {
            "name": row["name"],
            "code": row["code"],
            "description": row["description"],
            "visual_defaults": json.loads(row["visual_defaults"]),
            "metadata": json.loads(row["metadata"])
        }, axis=1).tolist()

    @staticmethod
    def process_products(df: pd.DataFrame) -> List[Dict]:
        return df.apply(lambda row: {
            "name": row["name"],
            "sku": row["sku"],
            "status": row["status"],
            "basePrice": float(row["basePrice"]),
            "currency": row["currency"],
            "family": row["family"],
            "specifications": json.loads(row["specifications"]),
            "visual_data": json.loads(row["visual_data"]),
            "metadata": json.loads(row["metadata"])
        }, axis=1).tolist()



'''
@app.post("/api/csv/batch-import")
async def batch_import_csvs(files: List[UploadFile]):
    results = {}
    
    for file in files:
        collection = file.filename.split('.')[0]
        if collection not in Collection.__members__:
            results[file.filename] = "Invalid collection name"
            continue
            
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        processor = CSVProcessor()
        processor_method = getattr(processor, f"process_{collection}")
        documents = processor_method(df)
        
        client = StrapiClient()
        success = []
        errors = []
        
        for doc in documents:
            try:
                result = await client.create_document(collection, doc)
                success.append(result)
            except Exception as e:
                errors.append({"data": doc, "error": str(e)})
                
        results[file.filename] = {
            "success": len(success),
            "errors": len(errors)
        }
        
    return results
'''
