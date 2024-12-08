from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CharacterAddPOSTRequest
from adapter import CharacterAdapter

class CharacterService:
    @staticmethod
    async def add(db: AsyncSession, character: dict) -> dict:
        """
        Creates a new character in the database.
        
        Args:
        db: app's db async session
        character: {id, name, height, mass, hair_color, skin_color, eye_color, brith_year}
        
        Returns:
        dict with created data.
        """
        validated_character_add_request = CharacterAddPOSTRequest(**character).dict()
            
        return await CharacterAdapter.add_characeter(
            db=db,
            character_data=validated_character_add_request
        )

    @staticmethod
    async def get_all(db: AsyncSession) -> list[dict]:
        """
        Retrieves all characters in db.
        
        Args:
        db: app's db async session
        
        Returns:
        list of dicts with character attributes(id, name, height, mass, eye_color, birth_year).
        """
        return await CharacterAdapter.get_all_characters(db=db)
    
    @staticmethod
    async def get_by_id(db: AsyncSession, id: int) -> dict:
        """
        Retrieves character by ID.
        
        Args:
        
        db: app's db async session
        id: int. Character's identifier.
        
        Returns:
        
        """
        return await CharacterAdapter.get_character_by_id(db=db, id=id)


    @staticmethod
    async def delete_by_id(db: AsyncSession, id: int) -> dict:
        """"
        Deletes Character based on ID.
        
        Args:
        db: app's db async session
        id: int. Character's identifier.
        
        returns:
        dict: {
            detail: Message indicating success of error.
        }
        """
        return await CharacterAdapter.delete_character_by_id(db=db, id=id)

        
        
