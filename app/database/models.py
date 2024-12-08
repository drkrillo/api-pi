from sqlalchemy import Column, Integer, String, Float
from database.config import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        autoincrement=False,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(100), 
        nullable=False,
        index=True,
        unique=True,
        comment="Unique character name."
    )
    height = Column(
        Integer, 
        index=True,
        nullable=True,
        comment="Height in cm."
    )
    mass = Column(
        Integer, 
        index=True,
        nullable=True,
        comment="Mass in kg."
    )
    hair_color = Column(
        String(20), 
        index=True,
        nullable=True,
        comment="Character's hair color."
    )
    skin_color = Column(
        String(20), 
        index=True,
        nullable=True,
        comment="Character's skin color."
    )
    eye_color = Column(
        String(20), 
        index=True,
        nullable=True,
        comment="Character's eye color."
    )
    birth_year = Column(
        Integer, 
        index=True,
        nullable=True,
        comment="Character's year of birth."
    )