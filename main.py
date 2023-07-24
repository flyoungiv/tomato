from typing import Union

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

# import psycopg2

# conn = psycopg2.connect(database = "postgres", user = "postgres", password = ";u/)Ahzy)\"ZE8Vc&", host = "34.121.201.240", port = "5432")

# cur = conn.cursor()

# cur.execute("SELECT id, name, age, medal  from contestants where id = '1'")
# rows = cur.fetchall()
# for row in rows:
#    print("ID = ", row[0])
#    print("NAME = ", row[1])
#    print("age = ", row[2])
#    print("medal = ", row[3], "\n")
# conn.close()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
