import pytest
from unittest.mock import AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from services import CharacterService
from adapter import CharacterAdapter

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
async def test_add():
    mock_db = AsyncMock(spec=AsyncSession)
    
    with patch.object(CharacterAdapter, 'add_characeter', new_callable=AsyncMock) as mock_add_character:
        mock_add_character.return_value = MOCK_CHARACTER

        result = await CharacterService.add(db=mock_db, character=MOCK_CHARACTER)
        
        mock_add_character.assert_called_once_with(
            db=mock_db,
            character_data=MOCK_CHARACTER
        )

        assert result == MOCK_CHARACTER

@pytest.mark.asyncio
async def test_get_all():
    mock_db = AsyncMock(spec=AsyncSession)
    
    with patch.object(CharacterAdapter, 'get_all_characters', new_callable=AsyncMock) as mock_get_all_characters:
        mock_get_all_characters.return_value = [
            MOCK_CHARACTER,
            MOCK_CHARACTER_2,
        ]

        result = await CharacterService.get_all(db=mock_db)
        
        mock_get_all_characters.assert_called_once_with(
            db=mock_db,
        )

        assert result == [
            MOCK_CHARACTER,
            MOCK_CHARACTER_2,
        ]


