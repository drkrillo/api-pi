import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models import Character


class CharacterRepository:
    
    @staticmethod
    async def get_all_characters(db: AsyncSession) -> List[Character]:
        result = await db.execute(select(Character))
        return result.scalars().all()
    
    @staticmethod
    async def get_character_by_name(db: AsyncSession, name: str) -> Character:
        result = await db.execute(select(Character).where(Character.name == name))
        return result.scalars().first()


    @staticmethod
    async def add_character(
        db: AsyncSession    ,
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

