# region API models
import re
import uuid

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from db.models import PortalRole

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert non dict obj-s to json"""

        orm_mode = True


class UserShowSecure(TunedModel):
    name: str
    surname: str
    email: EmailStr
    roles: list[PortalRole]


class UserShow(UserShowSecure):
    id: uuid.UUID
    is_active: bool


class UserCreate(BaseModel):
    name: str = Field(
        regex=LETTER_MATCH_PATTERN, description="Name must contain only letters"
    )
    surname: str = Field(
        regex=LETTER_MATCH_PATTERN, description="Surname must contain only letters"
    )
    email: EmailStr
    password: str


class UpdateUserRequest(BaseModel):
    name: str | None = Field(
        regex=LETTER_MATCH_PATTERN, description="Name must contain only letters"
    )
    surname: str | None = Field(
        regex=LETTER_MATCH_PATTERN, description="Name must contain only letters"
    )
    email: EmailStr | None


class Token(BaseModel):
    access_token: str
    token_type: str


# endregion
