from app.core.utils.loggers import setup_logger
from app.core.utils.enums import ServiceType
from app.services.unified.schema import PlatformCampaign

logger = setup_logger("meta/handler", "logs/meta.log")

async def create_meta_service_campaign(campaign_data, platform_campaign_id):
    try:
        campaign = PlatformCampaign(
            name=campaign_data.name,
            campaign_id=campaign_data.id,
            platform_campaign_id=platform_campaign_id,
            service_type=ServiceType.META,
            objective=campaign_data.objective,
            status=campaign_data.status
        )

        await campaign.insert()
        logger.info(f"Meta service campaign created: {campaign.id}")
        return campaign
    
    except Exception as e:  
        logger.error(f"Error creating meta service campaign with data -> {campaign_data}: {e}")
        return None