import uvicorn
import os
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, PositiveInt

from fastapi.middleware.cors import CORSMiddleware

from google.cloud.sql.connector import Connector, IPTypes
import pg8000

import sqlalchemy

import sqlalchemy
from sqlalchemy import text

# import psycopg2

DB_HOST = "34.121.201.240"
DB_USER = "postgres"
DB_PASSWORD = ";u/)Ahzy)\"ZE8Vc&"

app = FastAPI()

# CORS
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
def get_countries_list() -> list[OlympicCountry]:

  def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
      """Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL."""
      # Note: Saving credentials in environment variables is convenient, but not
      # secure - consider a more secure solution such as
      # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
      # keep secrets safe.
      db_user = DB_USER # os.environ["DB_USER"]  # e.g. 'my-database-user'
      db_pass = DB_PASSWORD # os.environ["DB_PASS"]  # e.g. 'my-database-password'
      db_name = 'postgres' # os.environ["DB_NAME"]  # e.g. 'my-database'
      unix_socket_path = 'symmetric-fold-393422:us-central1:tomato' #os.environ[
      "symmetric-fold-393422:us-central1:tomato"
      # ]  # e.g. '/cloudsql/project:region:instance'

      pool = sqlalchemy.create_engine(
          # Equivalent URL:
          # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
          sqlalchemy.engine.url.URL.create(
              # drivername="mysql+pymysql",
              drivername="postgresql+psycopg2",
              username=db_user,
              password=db_pass,
              database=db_name,
              query={"unix_socket": unix_socket_path},
          ),
          # ...
      )
      return pool

  engine = connect_unix_socket()

  with engine.connect() as conn:
      result = conn.execute(text("select 'hello world'"))
      print(result.all())

  return [{ "country:" "Algeria" }]

# use to get more in-depth detail on country
@app.get("/countries/{country_code}/detail")
def get_olympic_country_detail(country_code: int):
    return {"item_name": item.name, "country_code": country_code}

@app.get("/sqlalchemy")
def read_root():
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

    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())

    return { "message": "done"}

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0',
                port=os.environ['PORT'], log_level="info")
