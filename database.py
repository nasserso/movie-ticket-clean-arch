from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import Session

from settings import Settings


engine = create_engine(
    Settings().DATABASE_URL,
    isolation_level="SERIALIZABLE",
    poolclass=QueuePool,
)

def get_session():
    with Session(engine) as session:
        yield session
