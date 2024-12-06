import logging
from typing import List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models import Character
from app.exceptions.custom_exception import CharacterIdNotFound

class CharacterRepository:
    
    @staticmethod
    async def get_all_characters(db: AsyncSession) -> List[Character]:
        result = await db.execute(select(Character))
        return result.scalars().all()
    
    @staticmethod
    async def get_character_by_id(db: AsyncSession, id: int) -> Character:
        result = await db.execute(select(Character).where(Character.id == id))
        return result.scalars().first()

    @staticmethod
    async def add_character(
        db: AsyncSession,
        character_data: dict,
    ) -> Character:
        new_character = Character(**character_data)
        try:
            db.add(new_character)
            await db.commit()
            await db.refresh(new_character)
            return new_character
        
        except Exception as e:
            await db.rollback()
            logging.error(e)
            raise e

    @staticmethod
    async def delete_character_by_id(
        db: AsyncSession,
        id: int,
    ) -> dict:
        result = await db.execute(select(Character).where(Character.id == id))
        character_to_delete = result.scalars().first()

        if not character_to_delete:
            raise CharacterIdNotFound
        
        await db.execute(delete(Character).where(Character.id == id))
        await db.commit()

        return {"detail": f"Character with id {id} deleted successfully"}


