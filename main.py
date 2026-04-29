from fastapi import FastAPI

from apps.room.routers.routers import router

app = FastAPI()
app.include_router(router)
