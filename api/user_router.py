# region API Routes
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.actions.auth import get_current_user_from_token
from api.actions.user import _create_new_user
from api.actions.user import _delete_user
from api.actions.user import _get_user_by_id
from api.actions.user import _update_user
from api.actions.user import check_user_permissions
from api.schemas import UpdateUserRequest
from api.schemas import UserCreate
from api.schemas import UserShow
from api.schemas import UserShowSecure
from db.models import User
from db.session import get_async_session

user_router = APIRouter()


@user_router.post("/")
async def create_user(
    body: UserCreate, session: AsyncSession = Depends(get_async_session)
) -> UserShow:
    user = await _create_new_user(body, session)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {body.email} already exists.",
        )


@user_router.delete("/")
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token),
) -> UserShow:
    user_for_deletion = await _get_user_by_id(user_id, session)
    if not user_for_deletion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    if not check_user_permissions(
        target_user=user_for_deletion, current_user=current_user
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )
    user = await _delete_user(user_id, session)
    return user


@user_router.get("/")
async def get_user_by_id(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token),
) -> UserShow:
    user = await _get_user_by_id(user_id, session)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


@user_router.patch("/")
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_from_token),
) -> UserShow:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one parameter for user update info must provided.",
        )
    user_for_update = await _get_user_by_id(user_id, session)
    if not user_for_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    if not check_user_permissions(
        target_user=user_for_update, current_user=current_user
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )
    user = await _update_user(user_id, updated_user_params, session)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {body.email} already exists.",
        )


@user_router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user_from_token),
) -> UserShowSecure:
    return current_user


# endregion
