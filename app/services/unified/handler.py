from app.services.unified.schema import (User, LoginRequest, TokenResponse, Wallet, PlatformCampaignCreate,
                                         PlatformCampaign)
from passlib.context import CryptContext
from app.core.utils.enums import UserRole, WalletCurrency

# core utils imports
from app.core.utils.security import create_access_token
from app.core.utils.loggers import setup_logger

logger = setup_logger("unified/handler", "logs/unified.log")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def save_user_to_db(user: User):
    await user.insert()  # Save the user to the database
async def save_wallet_to_db(wallet: Wallet):
    await wallet.insert()  # Save the wallet to the database


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
        wallet = Wallet(
            user_id=str(user.id),
            balance=0.0,
            currency= WalletCurrency.USD
        )
        await user.insert()
        await wallet.insert()

        logger.info(f"User created: {str(user.id)}")
        logger.info(f"User wallet created: {str(wallet.id)}")

        return user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None

async def authenticate_user(user_data: LoginRequest):
    try:
        user  =  await User.find_one(User.email == user_data.email)
        if not user:
            logger.warning(f"User not found: {user_data.email}")
            return False
        
        if not pwd_context.verify(user_data.password, user.password):
            logger.warning(f"Invalid password for user: {user_data.email}")
            return False

        token = create_access_token({"sub": str(user.id), "email": user.email})
        if not token:
            return None
        logger.info(f"User authenticated: {str(user.id)}")
        return TokenResponse(access_token=token)
    
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        return None
    
async def create_campaign(type: str, campaign_data: PlatformCampaignCreate, user_id: str):
    try:
        if type.lower() == "platform":
            campaign = PlatformCampaign(
                name=campaign_data.name,
                user_id=user_id,
                description=campaign_data.description if campaign_data.description else '',
                total_budget=campaign_data.total_budget,
                status=campaign_data.status,
                start_date=campaign_data.start_date,
                end_date=campaign_data.end_date
            )

            await campaign.insert()
            logger.info(f"Platform Campaign created: {str(campaign.id)}")
            return campaign
        
    except Exception as e:
        logger.error(f"Error when creating a platform campaign for user with id -> {user_id} : {e}")
        return None