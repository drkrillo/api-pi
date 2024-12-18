import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from infrastructure import CharacterRepository
from exceptions.custom_exception import CharacterIdExistsError, CharacterIdNotFound

from exceptions.logger import logger


class CharacterAdapter:
    @staticmethod
    async def add_characeter(db: AsyncSession, character_data: dict) -> dict:
        """
        Is called by the service, and calls the repository.
        
        Args:
        db: app's db async session
        character_data: Dict with all Character¡s attributes.
        
        Returns:
        dict with all characters data.
        """
        character = await CharacterRepository.get_character_by_id(
            db=db,
            id=character_data["id"],
        )
        if character:
            logger.error(f"Character id {character.id} already exists.")
            raise CharacterIdExistsError("The ID is not available.")
        
        created_character = await CharacterRepository.add_character(
            db=db,
            character_data=character_data,
            )

        return {
            "id": created_character.id,
            "name": created_character.name,
            "height": created_character.height,
            "mass": created_character.mass,
            "hair_color": created_character.hair_color,
            "skin_color": created_character.skin_color,
            "eye_color": created_character.eye_color,
            "birth_year": created_character.birth_year,
        }

    @staticmethod
    async def get_all_characters(db: AsyncSession) -> List[dict]:
        """
        Is called by the service, and calls the repository.
        
        Args:
        db: app's db async session
        
        Returns:
        List[Dict(character_values)]
        """
        try:
            all_characters = await CharacterRepository.get_all_characters(db)
            all_characters = [
                {
                    'id': character.id,
                    'name': character.name,
                    'height': character.height,
                    'mass': character.mass,
                    'hair_color': character.hair_color,
                    'skin_color': character.skin_color,
                    'eye_color': character.eye_color,
                    'birth_year': character.birth_year
                }
                for character in all_characters
            ]
            return all_characters

        except Exception as e:
            logger.error(f"An error occurred while retrieving all characetrs: {e}")
            raise e

    async def get_character_by_id(db: AsyncSession, id: int) -> dict:
        """
        Is called by the service, and calls the repository.
        
        Args:
        db: app's db async session
        id: int. Character's identifier.
        
        Returns:
        Dict(detail: informative message)
        """
        selected_character = await CharacterRepository.get_character_by_id(db=db, id=id)
        if not selected_character:
            logger.error(f"Character ID {id} not found.")
            raise CharacterIdNotFound
        
        return {
            'id': selected_character.id,
            'name': selected_character.name,
            'height': selected_character.height,
            'mass': selected_character.mass,
            'hair_color': selected_character.hair_color,
            'skin_color': selected_character.skin_color,
            'eye_color': selected_character.eye_color,
            'birth_year': selected_character.birth_year
        }

    async def delete_character_by_id(db: AsyncSession, id: int):
        response = await CharacterRepository.delete_character_by_id(db=db, id=id)
        return response