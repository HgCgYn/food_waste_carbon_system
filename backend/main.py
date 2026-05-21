"""FastAPI entrypoint that wires API routes, CORS, and startup database setup."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.init_db import init_database
from routes import detect, records, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    yield


app = FastAPI(
    title="Food Waste Carbon System API",
    description="Detect food waste from plate images and estimate carbon emissions.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router, prefix="/api", tags=["detect"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(records.router, prefix="/api/records", tags=["records"])


@app.get("/", tags=["health"])
def root():
    return {"message": "Food Waste Carbon System API is running"}
