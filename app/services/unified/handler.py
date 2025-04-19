from app.services.unified.schema import User, LoginRequest, TokenResponse
from passlib.context import CryptContext
from app.core.utils.enums import UserRole

# core utils imports
from app.core.utils.jwt import create_access_token
from app.core.utils.loggers import setup_logger

logger = setup_logger("unified/handler", "logs/unified.log")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def save_user_to_db(user: User):
    await user.insert()  # Save the user to the database


async def create_user(user_data: User):
    try:
        hashed_password = pwd_context.hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            role = user_data.role if user_data.role else UserRole.ADVERTISER,
            password=hashed_password,
            full_name=user_data.full_name
        )
        await save_user_to_db(user)
        logger.info(f"User created: {str(user.id)}")
        return user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None

async def authenticate_user(user_data: LoginRequest):
    try:
        user  =  await User.find_one(User.email == user_data.email)
        print(user)
        if not user:
            logger.warning(f"User not found: {user_data.email}")
            return False
        
        if not pwd_context.verify(user_data.password, user.password):
            logger.warning(f"Invalid password for user: {user_data.email}")
            return False

        token = create_access_token({"sub": str(user.id), "email": user.email})
        logger.info(f"User authenticated: {str(user.id)}")
        return TokenResponse(access_token=token)
    
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        return None