import uvicorn
import os
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, PositiveInt

from fastapi.middleware.cors import CORSMiddleware

# import psycopg2

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

class OlympicCountry(BaseModel):
    country: str
    country_code: str
    medals: PositiveInt

@app.get("/")
def read_root():
    return {"Congratulations": "You found the backend"}

@app.get("/countries")
def read_item() -> list[OlympicCountry]:
    # conn = psycopg2.connect(database = "postgres", user = "postgres", password = ";u/)Ahzy)\"ZE8Vc&", host = "34.121.201.240", port = "5432")
    # cur = conn.cursor()

    # cur.execute("""
    # select
    #   p.country,
    #   cc.iso3 as country_code,
    #   count(1) as medals
    # from
    #   contestants c
    #   join country_codes cc on c.noc = cc.noc
    #   join populations p on cc.iso3 = p.country_code
    # where
    #   c.year >= 1960
    #   and c.year <= 2016
    #   and c.medal is not null
    # group by
    #   p.country,
    #   cc.iso3
    # order by
    #   country asc;
    # """)

    # rows = cur.fetchall()
    # conn.close()
    country1 = {
      "country": "Test1",
      "country_code": "AAA",
      "medals": 4
    }
    
    country1 = OlympicCountry(**country1)
    rows=[country1]
    # return {"item_id": item_id, "q": q}
    # olympic_countries = OlympicCountry(**rows)
    return rows

#use to get more in-depth detail on country
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=os.environ['PORT'], log_level="info")