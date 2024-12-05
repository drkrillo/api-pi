from pydantic import BaseModel, field_validator


class CharacterAddPOSTResponse(BaseModel):
    name: str
    height: float
    mass: float
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: int

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 200:
            raise ValueError("name must be 100 characters maximum.")
        return value
    
    @field_validator("height")
    def validate_height(cls, value):
        if value <= 0:
            raise ValueError("height must greater than 0")
        return value

    @field_validator("mass")
    def validate_mass(cls, value):
        if value <= 0:
            raise ValueError("mass must greater than 0")
        return value

    @field_validator("hair_color")
    def validate_hair_color(cls, value):
        if len(value) > 20:
            raise ValueError("hair color must be 20 characters maximum.")
        return value

    @field_validator("skin_color")
    def validate_skin_color(cls, value):
        if len(value) > 20:
            raise ValueError("skin color must be 20 characters maximum.")
        return value

    @field_validator("eye_color")
    def validate_eye_color(cls, value):
        if len(value) > 20:
            raise ValueError("eye color must be 20 characters maximum.")
        return value

class CharacterAllGETResponse(BaseModel):
    id: int
    name: str
    height: float
    mass: float
    birth_year: int
    eye_color: str
    
    @field_validator("id")
    def validate_name(cls, value):
        if value <= 0:
            raise ValueError("id must be bigger than 0.")
        return value

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 200:
            raise ValueError("name must be 100 characters maximum.")
        return value
    
    @field_validator("height")
    def validate_height(cls, value):
        if value <= 0:
            raise ValueError("height must greater than 0")
        return value

    @field_validator("mass")
    def validate_mass(cls, value):
        if value <= 0:
            raise ValueError("mass must greater than 0")
        return value
    
    @field_validator("eye_color")
    def validate_eye_color(cls, value):
        if len(value) > 20:
            raise ValueError("eye color must be 20 characters maximum.")
        return value
