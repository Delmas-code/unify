from app.services.unified.schema import (User, LoginRequest, TokenResponse, Wallet, PlatformCampaignCreate,
                                         PlatformCampaign)
from passlib.context import CryptContext
from app.core.utils.enums import UserRole, WalletCurrency
from app.core.utils.helper import stringify_id, parse_object_id
from beanie.operators import RegEx


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
            email=user_data.email.lower(),
            username=user_data.username.lower(),
            role = user_data.role if user_data.role else UserRole.ADVERTISER,
            password=hashed_password,
            full_name=user_data.full_name.lower()
        )
        await user.insert()

        wallet = Wallet(
            user_id=str(user.id),
            balance=0.0,
            currency= WalletCurrency.USD
        )
        await wallet.insert()

        logger.info(f"User created: {str(user.id)}")
        logger.info(f"User wallet created: {str(wallet.id)}")

        return user
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None

async def authenticate_user(user_data: LoginRequest):
    try:
        user  =  await User.find_one(User.username == user_data.username.lower())
        # user  =  await User.find_one(User.username.match(RegEx(user_data.username, case_sensitive=False)))

        if not user:
            logger.info(f"User not found: {user_data.username}")
            return False
        
        if not pwd_context.verify(user_data.password, user.password):
            logger.warning(f"Invalid password for user: {user_data.username}")
            return False

        token = create_access_token({"sub": str(user.id), "username": user.username})
        if not token:
            return None
        logger.info(f"User authenticated: {str(user.id)}")
        return TokenResponse(access_token=token)
    
    except Exception as e:
        logger.error(f"Error authenticating user: {e}")
        return None
    
async def get_user_by_id(user_id: str):
    try:
        user_id = parse_object_id(user_id)
        if not user_id:
            logger.warning(f"Invalid user id: {user_id}")
            return None
        user = await User.find_one(User.id == user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            return None
        return user
    except Exception as e:
        logger.error(f"Error getting user by id: {e}")
        return None

async def create_campaign(type: str, campaign_data: PlatformCampaignCreate, user_id: str):
    try:
        if type.lower() == "platform":
            campaign = PlatformCampaign(
                user_id=user_id,
                **campaign_data.model_dump(exclude_unset=True)
            )

            await campaign.insert()
            logger.info(f"Platform Campaign created: {str(campaign.id)}")
            return campaign
        
    except Exception as e:
        logger.error(f"Error when creating a platform campaign for user with id -> {user_id} : {e}")
        return None

async def get_all_campaigns(type: str ,user_id: str):
    try:
        if type.lower() == "platform":
            campaigns = await PlatformCampaign.find(PlatformCampaign.user_id == user_id).to_list()
            if not campaigns:
                logger.info(f"No Campaigns found for user with id: {user_id}")
                return []
            return campaigns
    except Exception as e:
        logger.error(f"Error getting campaigns: {e}")
        return None
    
async def get_campaign_by_id(campaign_id: str, user_id: str):
    try:
        campaign_id = parse_object_id(campaign_id)
        if not campaign_id:
            logger.warning(f"Invalid campaign id: {campaign_id}")
            return False, "not_found", "not found"
        
        campaign = await PlatformCampaign.find_one(PlatformCampaign.id == campaign_id)
        
        if not campaign:
            logger.warning(f"No Campaign found with id: {campaign_id}")
            return False, "not_found", "not found"
        
        if str(campaign.user_id) != str(user_id):
            logger.warning(f"Campaign with id: {campaign_id} does not belong to user with id: {user_id}")
            return False, "authorization_error", "not owned"
        
        return campaign, "success", "success"
    except Exception as e:
        logger.error(f"Error getting campaign with id -> {campaign_id}: {e}")
        return None, "error", e