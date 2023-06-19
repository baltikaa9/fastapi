from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from api.schemas import Token
from db.dals import UserDAL
from db.models import User
from db.session import get_async_session
from hashing import Hasher
from security import create_access_token

login_router = APIRouter()


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


@login_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login/token")


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


@login_router.get("/test_auth_endpoint")
async def sample_endpoint_under_jwt(
    current_user: User = Depends(get_current_user_from_token),
):
    return {"Success": True, "current_user": current_user}
