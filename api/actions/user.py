from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserCreate
from api.schemas import UserShow
from db.dals import UserDAL
from hashing import Hasher


async def _create_new_user(body: UserCreate, session: AsyncSession) -> UserShow | None:
    # async with session.begin():
    user_dal = UserDAL(session)
    user = await user_dal.create_user(
        name=body.name,
        surname=body.surname,
        email=body.email,
        hashed_password=Hasher.get_password_hash(body.password),
    )

    if user:
        return UserShow(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _delete_user(user_id: UUID, session: AsyncSession) -> UserShow | None:
    user_dal = UserDAL(session)
    user = await user_dal.delete_user(user_id)

    if user:
        return UserShow(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _get_user_by_id(user_id: UUID, session: AsyncSession) -> UserShow | None:
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_id(user_id)

    if user:
        return UserShow(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _update_user(
    user_id: UUID, updated_user_params: dict, session: AsyncSession
) -> UserShow | bool | None:
    user_dal = UserDAL(session)
    user = await user_dal.update_user(user_id, **updated_user_params)

    if user:
        return UserShow(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )
    elif user is False:
        return False
