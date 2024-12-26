from sqlmodel import SQLModel, create_engine

# TODO: usar postgres
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    # TODO: usar migrations
    SQLModel.metadata.create_all(engine)
