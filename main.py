from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import csv

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

data = []


with open('fixtures/data.csv', newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in file:
        print(row)
        data.append(', '.join(row))

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
