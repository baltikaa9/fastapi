# region Database models
from enum import Enum
from uuid import UUID
from uuid import uuid4

from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    ...


class PortalRole(str, Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_SUPER_ADMIN = "ROLE_SUPER_ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    roles: list[str] = Column(ARRAY(String), nullable=False)

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_ADMIN in self.roles

    @property
    def is_superadmin(self) -> bool:
        return PortalRole.ROLE_SUPER_ADMIN in self.roles


# endregion
