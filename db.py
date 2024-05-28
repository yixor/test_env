from sqlalchemy import create_engine
from settings import POSTGRES_URL


pg_engine = create_engine(POSTGRES_URL)
