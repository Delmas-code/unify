from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.core.utils.loggers import setup_logger

# importing all models(schema) for each service to ensure they are registered with Beanie
from app.services.unified.schema import (
    PlatformCampaign,
    ServiceCampaign,
    Transaction,
    Wallet,
    User,
    ServiceStatus,
    CampaignStatus,
)
from app.services.meta import schema as meta_schema

all_models = [
    User, Wallet, PlatformCampaign
]

db_logger = setup_logger('db/init_db', 'logs/database.log')

async def init_db(app):
    try:
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        db = client[settings.DATABASE_NAME]
        await init_beanie(database=db, document_models=all_models)

        # Store client in app state
        app.state.mongo_client = client
        
        db_logger.info("Database initialized successfully.")

    except Exception as e:
        db_logger.error(f"Error initializing database: {e}")
        raise e