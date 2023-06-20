from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserCreate
from db.dals import PortalRole
from db.dals import UserDAL
from db.models import User
from hashing import Hasher


async def _create_new_user(body: UserCreate, session: AsyncSession) -> User | None:
    # async with session.begin():
    user_dal = UserDAL(session)
    user = await user_dal.create_user(
        name=body.name,
        surname=body.surname,
        email=body.email,
        password=Hasher.get_password_hash(body.password),
        roles=[
            PortalRole.ROLE_USER,
        ],
    )
    return user


async def _delete_user(user_id: UUID, session: AsyncSession) -> User | None:
    user_dal = UserDAL(session)
    user = await user_dal.delete_user(user_id)
    return user


async def _get_user_by_id(user_id: UUID, session: AsyncSession) -> User | None:
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_id(user_id)
    return user


async def _update_user(
    user_id: UUID, updated_user_params: dict, session: AsyncSession
) -> User | bool | None:
    user_dal = UserDAL(session)
    user = await user_dal.update_user(user_id, **updated_user_params)
    return user


def check_user_permissions(target_user: User, current_user: User) -> bool:
    if target_user.is_superadmin:
        raise HTTPException(
            status_code=406, detail="Superadmin cannot be deleted via API."
        )
    if target_user.id != current_user.id:
        if not any((current_user.is_admin, current_user.is_superadmin)):
            return False
        if current_user.is_admin and target_user.is_admin:
            return False
    return True
