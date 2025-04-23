from fastapi import HTTPException
from app.core.utils.loggers import setup_logger

from app.services.unified.schema import PlatformCampaign
from app.core.utils.helper import parse_object_id
from app.services.meta.schema import MetaCampaignCreate, ServiceCampaign

async def create_meta_service_campaign(campaign_data, platform_campaign_id, current_user):
    
    # 1. Get the platform campaign
    platform_campaign = await PlatformCampaign.find_one({"_id": parse_object_id(platform_campaign_id)})
    
    if not platform_campaign:
        raise HTTPException(status_code=404, detail="Platform campaign not found")
    
    # 2. Check if Meta campaign exists
    existing = await ServiceCampaign.find_one({
        "platform_campaign_id": platform_campaign.id,
        "service_type": "META"
    })
    
    if existing:
        return existing
    
    # 3. Create campaign on Meta
    meta_campaign_id = await meta_client.create_campaign(campaign_data)
    
    # 4. Save in DB
    campaign = ServiceCampaign(
        name=campaign_data.name,
        meta_campaign_id=meta_campaign_id,
        platform_campaign_id=platform_campaign.id,
        service_type="META",
        objective=campaign_data.objective,
        status=campaign_data.status
    )
    
    await campaign.insert()
    
    return campaign