import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure import CharacterRepository
from app.exceptions.custom_exception import CharacterNameExistsError

from app.logger import logger


class CharacterAdapter:
    @staticmethod
    async def add_characeter(db: AsyncSession, character_data: dict) -> dict:
        character = await CharacterRepository.get_character_by_name(
            db=db,
            name=character_data["name"],
        )
        if character:
            raise CharacterNameExistsError("The name is not available.")
        
        created_character = await CharacterRepository.add_character(
            db=db,
            character_data=character_data,
            )

        return {
            "name": created_character.name,
            "height": created_character.height,
            "mass": created_character.mass,
            "hair_color": created_character.hair_color,
            "skin_color": created_character.skin_color,
            "eye_color": created_character.eye_color,
            "birth_year": created_character.birth_year,
        }

    @staticmethod
    async def get_all_characters(db: AsyncSession):
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
            logging.error(e)
            raise e


