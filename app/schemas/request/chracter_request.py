from pydantic import BaseModel, validator


class CharacterAddPOSTRequest(BaseModel):
    name: str
    height: float
    mass: float
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: int


    @validator("name")
    def validate_name(cls, value):
        if len(value) > 200:
            raise ValueError("name must be 100 characters maximum.")
        return value
    
    @validator("height")
    def validate_height(cls, value):
        if value <= 0:
            raise ValueError("height must greater than 0")
        return value

    @validator("mass")
    def validate_mass(cls, value):
        if value <= 0:
            raise ValueError("mass must greater than 0")
        return value

    @validator("hair_color")
    def validate_hair_color(cls, value):
        if len(value) > 20:
            raise ValueError("hair color must be 20 characters maximum.")
        return value

    @validator("skin_color")
    def validate_skin_color(cls, value):
        if len(value) > 20:
            raise ValueError("skin color must be 20 characters maximum.")
        return value

    @validator("eye_color")
    def validate_eye_color(cls, value):
        if len(value) > 20:
            raise ValueError("eye color must be 20 characters maximum.")
        return value

