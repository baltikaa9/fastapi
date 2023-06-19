# region API Routes
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UpdateUserRequest
from api.schemas import UserCreate
from api.schemas import UserShow
from db.dals import UserDAL
from db.session import get_async_session

user_router = APIRouter()


async def _create_new_user(body: UserCreate, session: AsyncSession) -> UserShow | None:
    # async with session.begin():
    user_dal = UserDAL(session)
    user = await user_dal.create_user(
        name=body.name, surname=body.surname, email=body.email
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


@user_router.post("/")
async def create_user(
    body: UserCreate, session: AsyncSession = Depends(get_async_session)
) -> UserShow:
    user = await _create_new_user(body, session)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=409, detail=f"User with email {body.email} already exists."
        )


@user_router.delete("/")
async def delete_user(
    user_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> UserShow:
    user = await _delete_user(user_id, session)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )


@user_router.get("/")
async def get_user_by_id(
    user_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> UserShow:
    user = await _get_user_by_id(user_id, session)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )


@user_router.patch("/")
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    session: AsyncSession = Depends(get_async_session),
) -> UserShow:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info must provided.",
        )
    user = await _update_user(user_id, updated_user_params, session)
    if user:
        return user
    elif user is False:
        raise HTTPException(
            status_code=409, detail=f"User with email {body.email} already exists."
        )
    elif user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )


# endregion
