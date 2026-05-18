import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import sessionmaker
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "build" / ".env"

# Load database connection parameters from .env file
load_dotenv(ENV_PATH)

def get_url_from_env():
    driver_name = getenv("PGSYNCDRIVER")
    username = getenv("PGROLE")
    password = getenv("PGPASSWORD")
    host = getenv("PGHOST")
    port = getenv("PGPORT")
    database = getenv("PGDATABASE")

    if not all([driver_name, username, password, host, port, database]):
        raise RuntimeError("Missing required env vars for database connection")

    return make_url(f"{driver_name}://{username}:{password}@{host}:{port}/{database}")

# Create SQLAlchemy session factory
Session = sessionmaker(bind=create_engine(get_url_from_env()))