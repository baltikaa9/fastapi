# region Database models
import uuid

from sqlalchemy import Column, String, UUID, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(), nullable=False)
    surname = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)


# endregion