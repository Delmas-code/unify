from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.core.config import settings
from app.core.utils.loggers import setup_logger

from app.services.unified.schema import TokenData, User

logger = setup_logger("core/utils/security", "logs/core_utils.log")
def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    except Exception as e:
        logger.error(f"Error encoding login token: {e}")
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exceptions = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials or token expired",
        headers= {"WWW-Authenticate": "Bearere"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        exp: int = payload.get("exp")

        if email is None or user_id is None:
            logger.warning(f"Error email or user id is missing in token decoded")
            raise credential_exceptions
        if datetime.now(timezone.utc)> exp:
            logger.warning(f"Error token has expired")
            raise credential_exceptions
        
        token_data = TokenData(id=user_id, email=email)
        user = await User.find_one(User.id == token_data.id)
        if user is None:
            logger.error(f"Error user with id in token was not found")
            raise credential_exceptions

        return user
    except JWTError as e:
        logger.error(f"Error with JWT decoding: {e}")
        raise credential_exceptions
    except Exception as e:
        logger.error(f"Error occured while getting current user: {e}")
        raise credential_exceptions