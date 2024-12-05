import asyncio
import logging
from typing import Optional, List
from functools import wraps

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.reflection import Inspector

from app.database.config import Base, engine, get_db
from app.services import CharacterService
from app.schemas import (
    CharacterAddPOSTResponse,
    CharacterAddPOSTRequest,
    CharacterAllGETResponse,
)
from app.exceptions.custom_exception import CharacterNameExistsError
from app.logger import logger


app = FastAPI(
    title="Character Machine",
    description="API to manage characters.",
    version="0.1.0",
    docs_url="/",
)

API_VERSION = 'v1'


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CharacterNameExistsError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
    return wrapper

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("SQLite database initialized and tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize the database: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """Se ejecuta al iniciar la aplicación"""
    await init_db()

@app.get(
    f"/{API_VERSION}/test",
    response_model=None,
    status_code=200
)
async def test_api(session: AsyncSession = Depends(get_db)):
    async with engine.connect() as connection:
        def sync_inspection(sync_connection):
            inspector = inspect(sync_connection)
            tables = inspector.get_table_names()
            database_schema = {}
            for table in tables:
                columns = inspector.get_columns(table)
                foreign_keys = inspector.get_foreign_keys(table)
                database_schema[table] = {
                    "columns": [{col['name']: col['type']} for col in columns],
                    "foreign_keys": foreign_keys,
                }
            return database_schema

        database_schema = await connection.run_sync(sync_inspection)

    return {
        "status": "ok",
        "database_schema": database_schema,
    }

@app.get(
    f"/{API_VERSION}/character/getAll",
    response_model=List[CharacterAllGETResponse],
    status_code=200
)
async def character_getall_endpoint(db: AsyncSession = Depends(get_db)):

    service_characters = await CharacterService.get_all(db)
    try:
        return [
            CharacterAllGETResponse(**character)
            for character in service_characters
        ]
    except Exception as e:
        logger.error(f"Error while retrieving all characeters: {e}")
        return HTTPException(status_code=400, detail=f"Error while retrieving all characters: {e}")

@app.post(
    f"/{API_VERSION}/character/add",
    response_model=CharacterAddPOSTResponse,
    status_code=200
)
@handle_exceptions
async def character_post_endpoint(
    post_request: CharacterAddPOSTRequest,
    db: AsyncSession = Depends(get_db),
):
    added_character = await CharacterService.add(
        db=db,
        character=post_request.dict(),
    )
    return CharacterAddPOSTResponse(**added_character)

if __name__ == "__main__":
    asyncio.run(init_db())