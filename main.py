from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    user_id: str
    site: str
    violation: str
    risk: int
    time: str

data_store = []

@app.get("/")
def home():
    return {"message": "PPE Cloud Running"}

@app.post("/violation")
def receive(data: Data):
    data_store.append(data)
    return {"status": "ok"}

@app.get("/data")
def get_data():
    return data_store