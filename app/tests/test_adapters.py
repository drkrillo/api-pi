import pytest
from unittest.mock import AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from services import CharacterService
from adapter import CharacterAdapter
from infrastructure import CharacterRepository
from exceptions.custom_exception import CharacterIdExistsError

MOCK_CHARACTER = {
    "id": 1,
    "name": "Frodo",
    "height": 100,
    "mass": 60,
    "hair_color": "black",
    "skin_color": "white",
    "eye_color": "blue",
    "birth_year": 500,
}

MOCK_CHARACTER_2 = {
    "id": 15,
    "name": "Pippin",
    "height": 90,
    "mass": 65,
    "hair_color": "brown",
    "skin_color": "pink",
    "eye_color": "brown",
    "birth_year": 495,
}

@pytest.mark.asyncio
async def test_add_character_success():
    mock_db = AsyncMock(spec=AsyncSession)
    
    mock_character = AsyncMock()
    mock_character.id = MOCK_CHARACTER["id"]
    mock_character.name = MOCK_CHARACTER["name"]
    mock_character.height = MOCK_CHARACTER["height"]
    mock_character.mass = MOCK_CHARACTER["mass"]
    mock_character.hair_color = MOCK_CHARACTER["hair_color"]
    mock_character.skin_color = MOCK_CHARACTER["skin_color"]
    mock_character.eye_color = MOCK_CHARACTER["eye_color"]
    mock_character.birth_year = MOCK_CHARACTER["birth_year"]

    with patch.object(CharacterRepository, 'get_character_by_id', AsyncMock(return_value=None)) as mock_get_character_by_id, \
         patch.object(CharacterRepository, 'add_character', AsyncMock(return_value=mock_character)) as mock_add_character:

        result = await CharacterAdapter.add_characeter(
            db=mock_db,
            character_data=MOCK_CHARACTER,
        )
        
        mock_get_character_by_id.assert_called_once_with(
            db=mock_db,
            id=MOCK_CHARACTER["id"]
        )

        mock_add_character.assert_called_once_with(
            db=mock_db,
            character_data=MOCK_CHARACTER
        )

        assert result == MOCK_CHARACTER

@pytest.mark.asyncio
async def test_add_character_exists_error():
    mock_db = AsyncMock(spec=AsyncSession)
    
    mock_character = AsyncMock()
    mock_character.id = MOCK_CHARACTER["id"]
    mock_character.name = MOCK_CHARACTER["name"]
    mock_character.height = MOCK_CHARACTER["height"]
    mock_character.mass = MOCK_CHARACTER["mass"]
    mock_character.hair_color = MOCK_CHARACTER["hair_color"]
    mock_character.skin_color = MOCK_CHARACTER["skin_color"]
    mock_character.eye_color = MOCK_CHARACTER["eye_color"]
    mock_character.birth_year = MOCK_CHARACTER["birth_year"]

    with patch.object(CharacterRepository, 'get_character_by_id', AsyncMock(return_value=mock_character)) as mock_get_character_by_id, \
         patch.object(CharacterRepository, 'add_character', AsyncMock(return_value=None)) as mock_add_character:

        with pytest.raises(
            CharacterIdExistsError, 
            match="The ID is not available."
        ):
            await CharacterAdapter.add_characeter(
                db=mock_db,
                character_data=MOCK_CHARACTER,
            )
        
        mock_get_character_by_id.assert_called_once_with(
            db=mock_db,
            id=MOCK_CHARACTER["id"]
        )

        mock_add_character.assert_not_called()
    