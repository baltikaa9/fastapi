from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import UserDAL
from db.models import User
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
