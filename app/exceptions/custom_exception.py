
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