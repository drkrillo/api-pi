import asyncio
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_db
from services import CharacterService
from schemas import (
    CharacterAddPOSTResponse,
    CharacterAddPOSTRequest,
    CharacterAllGETResponse,
    CharacterByIdGETResponse,
)
from exceptions.custom_exception import handle_exceptions

API_VERSION = 'v1'

router = APIRouter(prefix=f"/{API_VERSION}/character", tags=["character"])

@router.get(
    "/getAll",
    response_model=List[CharacterAllGETResponse],
    status_code=200
)
@handle_exceptions
async def character_get_all_endpoint(db: AsyncSession = Depends(get_db)):
    all_characters = await CharacterService.get_all(db)
    return [
        CharacterAllGETResponse(**character)
        for character in all_characters
    ]

@router.get(
    f"/get/{{id}}",
    response_model=CharacterByIdGETResponse,
    status_code=200
)
@handle_exceptions
async def character_get_by_id_endpoint(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    selected_character = await CharacterService.get_by_id(db=db, id=id)
    return CharacterByIdGETResponse(**selected_character)

@router.post(
    "/add",
    response_model=CharacterAddPOSTResponse,
    status_code=200
)
@handle_exceptions
async def character_post_add_endpoint(
    post_request: CharacterAddPOSTRequest,
    db: AsyncSession = Depends(get_db),
):
    added_character = await CharacterService.add(
        db=db,
        character=post_request.dict(),
    )
    return CharacterAddPOSTResponse(**added_character)

@router.delete(
    f"/delete/{{id}}",
    response_model=None,
    status_code=200
)
@handle_exceptions
async def character_delete_by_id_endpoint(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    response = await CharacterService.delete_by_id(db=db, id=id)
    return JSONResponse(response)
