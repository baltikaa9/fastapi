# region Interaction with database in business context
from enum import Enum
from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class PortalRole(str, Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_SUPER_ADMIN = "ROLE_SUPER_ADMIN"


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        email: str,
        password: str,
        roles: list[PortalRole],
    ) -> User | None:
        statement = (
            update(User)
            .where((User.email == email) & (User.is_active == False))
            .values(is_active=True)
            .returning(User)
        )
        user = await self.db_session.execute(statement)
        await self.db_session.commit()
        user = user.fetchone()
        if user:
            return user[0]

        else:
            new_user = User(
                name=name, surname=surname, email=email, password=password, roles=roles
            )
            self.db_session.add(new_user)
            # await self.db_session.flush()
            try:
                await self.db_session.commit()
                return new_user
            except IntegrityError:
                """if email is occupied"""
                return

    async def delete_user(self, user_id: UUID) -> User | None:
        return await self.update_user(user_id, is_active=False)

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where((User.id == user_id) & (User.is_active == True))
        user = await self.db_session.execute(query)
        # await self.db_session.commit()
        user = user.fetchone()
        if user:
            return user[0]

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where((User.email == email) & (User.is_active == True))
        user = await self.db_session.execute(query)
        # await self.db_session.commit()
        user = user.fetchone()
        if user:
            return user[0]

    async def update_user(self, user_id: UUID, **kwargs) -> User | bool | None:
        statement = (
            update(User)
            .where((User.id == user_id) & (User.is_active == True))
            .values(kwargs)
            .returning(User)
        )
        try:
            user = await self.db_session.execute(statement)
        except IntegrityError:
            return False
        await self.db_session.commit()
        user = user.fetchone()
        if user:
            return user[0]


# endregion
