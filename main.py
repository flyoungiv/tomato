from typing import Union
from csv import DictReader

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

data = []

with open('fixtures/data.csv', newline='') as csvfile:
    dict_reader = DictReader(csvfile)   
    data = list(dict_reader)

@app.get("/")
def read_root():
    # return {"Hello": "World"}
    return data


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
