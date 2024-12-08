from typing import List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Character
from exceptions.custom_exception import CharacterIdNotFound

from exceptions.logger import logger


class CharacterRepository:
    
    @staticmethod
    async def get_all_characters(db: AsyncSession) -> List[Character]:
        """
        Interacts with DB to retrieve all characters.
        
        Args:
        db: app's db async session
        
        Returns:
        List[Character]
        """
        result = await db.execute(select(Character))
        return result.scalars().all()
    
    @staticmethod
    async def get_character_by_id(db: AsyncSession, id: int) -> Character:
        """
        Interacts with db to retrieve character by ID.
        
        Args:
        db: app's db async session
        id: int. Character's identifier.
        
        Returns:
        Character.
        """
        result = await db.execute(select(Character).where(Character.id == id))
        return result.scalars().first()

    @staticmethod
    async def add_character(
        db: AsyncSession,
        character_data: dict,
    ) -> Character:
        """
        Interacts with db to add character.
        
        Args:
        db: app's db async session
        character_data: dict. All character's attributes.
        
        Returns:
        Character.
        """
        new_character = Character(**character_data)
        try:
            db.add(new_character)
            await db.commit()
            await db.refresh(new_character)
            return new_character
        
        except Exception as e:
            await db.rollback()
            logger.error(f"An error ocurred while traying to create new character: {e}")
            raise e

    @staticmethod
    async def delete_character_by_id(
        db: AsyncSession,
        id: int,
    ) -> dict:
        """
        Interacts with db to delete character by ID.
        
        Args:
        db: app's db async session
        id: int. Characetr's identifier.
        
        Returns:
        dict {detail: Message}
        """
        result = await db.execute(select(Character).where(Character.id == id))
        character_to_delete = result.scalars().first()

        if not character_to_delete:
            logger.error(f"Character ID {id} not found.")
            raise CharacterIdNotFound
        
        await db.execute(delete(Character).where(Character.id == id))
        await db.commit()

        return {"detail": f"Character with id {id} deleted successfully"}
    