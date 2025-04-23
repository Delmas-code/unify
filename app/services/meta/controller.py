from fastapi import HTTPException
from app.core.utils.loggers import setup_logger
from app.services.unified.schema import PlatformCampaign


logger = setup_logger("meta/controller", "logs/meta.log")

async def create_meta_campaign(campaign_data, platform_campaign_id, current_user):
    platform_campaign = await PlatformCampaign.get(platform_campaign_id)
    if not platform_campaign:
        logger.info(f"Platform campaign with ID {platform_campaign_id} not found")
        raise HTTPException(status_code=404, detail="Platform campaign not found")