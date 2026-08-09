from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.routes import items, members, loans

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app= FastAPI(title="Library Management API", lifespan=lifespan)
app.include_router(items.router)
app.include_router(members.router)
app.include_router(loans.router)

@app.get("/")
async def root():
    return {"message": "Library API is running"}