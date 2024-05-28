from typing import TypeAlias
seconds: TypeAlias = int

DOCKER = True

REVIEWS_PER_PAGE: int = 8
REDIS_CACHE_EXPIRES: seconds = 500

if DOCKER:
    import os

    ALEMBIC_INI = "alembic_docker.ini"

    DATA_PATH = os.environ.get("DATA_PATH")

    APP_HOST = os.environ.get("HOST_ADDRESS")
    APP_PORT = os.environ.get("PORT")

    POSTGRES_URL = os.environ.get("DB_URL")

    REDIS_CONFIG = {
        "host": os.environ.get("REDIS_HOST"),
        "port": os.environ.get("REDIS_PORT"),
        "db": os.environ.get("REDIS_DB")
    }
else:
    ALEMBIC_INI = "alembic.ini"

    DATA_PATH = "./data/"

    APP_HOST = "127.0.0.1"
    APP_PORT = 8000

    POSTGRES_URL = "postgresql://postgres@localhost:5432/postgres"

    REDIS_CONFIG = {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 0
    }
