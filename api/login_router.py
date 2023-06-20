from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from api.actions.auth import authenticate_user
from api.actions.auth import get_current_user_from_token
from api.schemas import Token
from db.models import User
from db.session import get_async_session
from security import create_access_token

login_router = APIRouter()


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


@login_router.get("/test_auth_endpoint")
async def sample_endpoint_under_jwt(
    current_user: User = Depends(get_current_user_from_token),
):
    return {"Success": True, "current_user": current_user}
