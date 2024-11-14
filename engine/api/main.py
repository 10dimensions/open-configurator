# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pricing")
def compute_price():
    return {"price": 10}
