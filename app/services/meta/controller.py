from fastapi import HTTPException
from app.core.utils.loggers import setup_logger

from app.services.unified.schema import PlatformCampaign
from app.core.utils.helper import parse_object_id
from app.services.meta.handler import create_meta_service_campaign
from app.services.meta.client import meta_client

logger = setup_logger("meta/controller", "logs/meta.log")

async def create_meta_campaign(campaign_data, platform_campaign_id, current_user):
    try:
        #1: get platform campaign
        
        platform_campaign_id = parse_object_id(platform_campaign_id)

        if not platform_campaign_id:
            logger.warning(f"Invalid campaign id: {platform_campaign_id}")
            raise HTTPException(status_code=400, detail="Invalid campaign id")

        platform_campaign = await PlatformCampaign.find_one({"_id": platform_campaign_id})
        if not platform_campaign:
            logger.warning(f"No platform campaign found with id: {platform_campaign_id}")
            raise HTTPException(status_code=404, detail="Platform campaign not found")

        #2: check if platform campaign belongs to the user
        user_id = str(current_user.id)
        if str(platform_campaign.user_id) != user_id:
            logger.warning(f"Campaign with id: {str(platform_campaign.id)} does not belong to user with id: {user_id}")
            raise HTTPException(status_code=403, detail="Campaign not owned by this user")
        
        #3: create service campaign on meta
        service_campaign = meta_client.create_campaign(campaign_data)
        if not service_campaign:
            logger.error(f"Failed to create campaign on meta: {campaign_data}")
            raise HTTPException(status_code=500, detail="Failed to create campaign on meta")
            
        #4: save the serivce campaign in the db
        campaign = await create_meta_service_campaign(service_campaign, platform_campaign_id)
        if not campaign:
            return service_campaign, False
        
        #5: return the service campaign
        return campaign, True

        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    """
    platform_campaign_id = parse_object_id(platform_campaign_id)
    if not platform_campaign_id:
        logger.info(f"Invalid platform campaign ID: {platform_campaign_id}")
        raise HTTPException(status_code=400, detail="Invalid platform campaign ID")
    
    platform_campaign_id = PlatformCampaign.find_one({"_id": platform_campaign_id})

    if not platform_campaign:
        logger.info(f"Platform campaign with ID {platform_campaign_id} not found")
        raise HTTPException(status_code=404, detail="Platform campaign not found")
        """