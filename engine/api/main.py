# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional

from store import Collection, Document, StrapiClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/pricing")
def compute_price():
    return {"price": 10}


# API endpoints
@app.post("/api/{collection}", response_model=Dict)
async def create_document(collection: Collection, document: Document):
    client = StrapiClient()
    return await client.create_document(collection.value, document.data)

@app.put("/api/{collection}/{id}", response_model=Dict)
async def update_document(collection: Collection, id: int, document: Document):
    client = StrapiClient()
    return await client.update_document(collection.value, id, document.data)

@app.post("/api/batch/{collection}", response_model=BulkResponse)
async def batch_create_documents(collection: Collection, documents: List[Document]):
    client = StrapiClient()
    success = []
    errors = []
    
    for doc in documents:
        try:
            result = await client.create_document(collection.value, doc.data)
            success.append(result)
        except Exception as e:
            errors.append({"data": doc.data, "error": str(e)})
            
    return BulkResponse(success=success, errors=errors)

@app.post("/api/csv/import/{collection}")
async def import_csv(
    collection: Collection,
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
        
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    #processor = CSVProcessor()
    #processor_method = getattr(processor, f"process_{collection.value.replace('-', '_')}")
    #documents = processor_method(df)
    
    documents = df.to_dict('records')

    async def process_documents():
        client = StrapiClient()
        for doc in documents:
            try:
                await client.create_document(collection.value, doc)
            except Exception as e:
                print(f"Error processing document: {e}")
                
    background_tasks.add_task(process_documents)
    
    return {"message": f"Processing {len(documents)} documents in background"}
