import asyncio
import logging
from typing import List

from fastapi import FastAPI
from sqlalchemy import inspect

from database.config import Base, engine, init_db

from exceptions.logger import logger
from routers import rest_endpoints

app = FastAPI(
    title="Character Machine",
    description="API to manage characters.",
    version="0.1.0",
    docs_url="/",
)

app.include_router(rest_endpoints.router)

@app.on_event("startup")
async def startup_event():
    """Executes when app starts."""
    await init_db()

if __name__ == "__main__":
    asyncio.run(init_db())