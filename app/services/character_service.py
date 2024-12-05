import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CharacterAddPOSTRequest
from app.adapter import CharacterAdapter
from app.logger import logger
from app.exceptions.custom_exception import CharacterNameExistsError

class CharacterService:
    @staticmethod
    async def add(db: AsyncSession, character: dict) -> dict:
        validated_character_add_request = CharacterAddPOSTRequest(**character).dict()
            
        return await CharacterAdapter.add_characeter(
            db=db,
            character_data=validated_character_add_request
        )

    @staticmethod
    async def get_all(db: AsyncSession) -> dict:
        return await CharacterAdapter.get_all_characters(db)

        
        
