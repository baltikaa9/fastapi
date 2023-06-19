# region API models
import re
import uuid

from pydantic import BaseModel, EmailStr, Field

LETTER_MATCH_PATTERN = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert non dict obj-s to json"""

        orm_mode = True


class UserShow(TunedModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str = Field(regex=LETTER_MATCH_PATTERN, description='Name must contain only letters')
    surname: str = Field(regex=LETTER_MATCH_PATTERN, description='Surname must contain only letters')
    email: EmailStr


class UpdateUserRequest(BaseModel):
    name: str | None = Field(regex=LETTER_MATCH_PATTERN, description='Name must contain only letters')
    surname: str | None = Field(regex=LETTER_MATCH_PATTERN, description='Name must contain only letters')
    email: EmailStr | None


# endregion