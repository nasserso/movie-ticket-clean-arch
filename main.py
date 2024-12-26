from fastapi import FastAPI

from apps.room.routers.routers import router
from database import create_db_and_tables

app = FastAPI()
app.include_router(router)

def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()
