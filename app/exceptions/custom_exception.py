from functools import wraps
from fastapi import HTTPException


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CharacterIdExistsError as e:
            raise HTTPException(status_code=400, detail="Character ID already exists.")
        except CharacterIdNotFound as e:
            raise HTTPException(status_code=400, detail="Character ID not found.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
    return wrapper

class CharacterIdExistsError(Exception):
    """
    This exception is raised when a new character
    chooses a existing name.
    """
    pass

class CharacterIdNotFound(Exception):
    """
    This exception is raised when trying
    to get a character by id but it doesn't 
    exist.
    """
    pass