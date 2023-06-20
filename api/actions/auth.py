from fastapi import Depends
from fastapi import HTTPException
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from api.login_router import oauth2_schema
from db.dals import UserDAL
from db.models import User
from db.session import get_async_session
from hashing import Hasher


async def _get_user_by_email_for_auth(email: str, session: AsyncSession) -> User | None:
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_email(email)


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> User | None:
    user = await _get_user_by_email_for_auth(email, session)
    if not user:
        return
    return user if Hasher.verify_password(password, user.hashed_password) else None


async def get_current_user_from_token(
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_async_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email, session)
    if user:
        return user
