import uvicorn
import os
from typing import Union
from pydantic import BaseModel, PositiveInt

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy
from sqlalchemy import text

DB_HOST = "34.121.201.240"
DB_USER = "postgres"
DB_PASSWORD = ";u/)Ahzy)\"ZE8Vc&"

app = FastAPI()

# CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://tomato-frontend-react.vercel.app",
    "https://tomato-frontend-angular.vercel.app"
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
    population: float
    ratio: float

class OlympicSeries(BaseModel):
    year: str
    medals: float
    population: float

class OlympicCountryDetails(BaseModel):
    country_code: str
    series: list[OlympicSeries]


@app.get("/")
def read_root():
    return {"Congratulations": "You found the backend"}

@app.get("/all-countries")
def get_all_countries() -> list[OlympicCountry]:
    import os

    def connect_with_connector() -> sqlalchemy.engine.base.Engine:
        """
        Initializes a connection pool for a Cloud SQL instance of Postgres.

        Uses the Cloud SQL Python Connector package.
        """
        # Note: Saving credentials in environment variables is convenient, but not
        # secure - consider a more secure solution such as
        # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
        # keep secrets safe.

        instance_connection_name = 'symmetric-fold-393422:us-central1:tomato'
        # e.g. 'project:region:instance'
        db_user = DB_USER  # e.g. 'my-db-user'
        db_pass = DB_PASSWORD  # e.g. 'my-db-password'
        db_name = 'postgres'  # e.g. 'my-database'

        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

        # initialize Cloud SQL Python Connector object
        connector = Connector()

        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name,
                ip_type=ip_type,
            )
            return conn

        # The Cloud SQL Python Connector can be used with SQLAlchemy
        # using the 'creator' argument to 'create_engine'
        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            # ...
        )

        return pool

    engine = connect_with_connector()
    
    rows = []

    with engine.connect() as conn:
        result = conn.execute(text("""
            select
                p.country,
                cc.iso3 as country_code,
                count(1) as medals,
                p.population
            from
                contestants c
                join country_codes cc on c.noc = cc.noc
                join populations p on cc.iso3 = p.country_code
            where
                c.medal is not null
                and p.year = '2016'
            group by
                p.country,
                p.population,
                cc.iso3
            order by
                country asc;
            """))
        
        rows = result.all()

    countries = []

    for row in rows:

        medals = float(row[2])
        population = round(float(row[3]) / 10000000, 2)

        country = {
            "country": row[0],
            "country_code": row[1],
            "medals": medals,
            "population": population,
            "ratio": round(medals / population, 2)
        }

        country = OlympicCountry(**country)
        countries.append(country)

    return countries

# use to get more in-depth detail on country
@app.get("/countries/{country_code}/detail")
def get_details_by_country(country_code: str) -> OlympicCountryDetails:
    import os

    def connect_with_connector() -> sqlalchemy.engine.base.Engine:
        """
        Initializes a connection pool for a Cloud SQL instance of Postgres.

        Uses the Cloud SQL Python Connector package.
        """
        # Note: Saving credentials in environment variables is convenient, but not
        # secure - consider a more secure solution such as
        # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
        # keep secrets safe.

        instance_connection_name = 'symmetric-fold-393422:us-central1:tomato'
        # e.g. 'project:region:instance'
        db_user = DB_USER  # e.g. 'my-db-user'
        db_pass = DB_PASSWORD  # e.g. 'my-db-password'
        db_name = 'postgres'  # e.g. 'my-database'

        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

        # initialize Cloud SQL Python Connector object
        connector = Connector()

        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name,
                ip_type=ip_type,
            )
            return conn

        # The Cloud SQL Python Connector can be used with SQLAlchemy
        # using the 'creator' argument to 'create_engine'
        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            # ...
        )

        return pool

    engine = connect_with_connector()
    
    rows = []

    with engine.connect() as conn:
        result = conn.execute(text(f"""
            select
                cc.iso3 as country_code,
                p.year,
                p.population,
                count(1) as medals
            from
                contestants c
                join country_codes cc on c.noc = cc.noc
                join populations p on cc.iso3 = p.country_code and c.year = cast(p.year as integer)
            where
                c.year >= 1960
                and c.year <= 2016
                and c.medal is not null
                and cc.iso3 = '{country_code}'
            group by
                cc.iso3,
                p.year,
                p.population
            order by
                cc.iso3 asc;
            """))
        
        rows = result.all()

    series = []

    for row in rows:

        medals = float(row[3])
        population = round(float(row[2]) / 10000000, 2)

        series_data = {
            "year": row[1],
            "medals": medals,
            "population": population
        }

        series.append(OlympicSeries(**series_data))

    country_details = {
        "country_code": country_code,
        "series": series
    }

    print(country_details)

    country_details = OlympicCountryDetails(**country_details)
    
    return country_details

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0',
                port=os.environ['PORT'], log_level="info")
