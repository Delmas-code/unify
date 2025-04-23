from app.services.meta.schema import MetaCampaignCreate
from app.services.unified.schema import User
from app.core.utils.security import get_current_user

from app.services.meta.controller import create_meta_campaign
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/meta/service-campaign/")
async def create_meta_service_campaign(
    campaign_data: MetaCampaignCreate,
    platform_campaign_id: str,
    current_user: User = Depends(get_current_user),
):
    campaign = create_meta_campaign(campaign_data, platform_campaign_id, current_user)
    # return campaign

    # 1. Get the platform campaign
    

    # 2. Check if Meta campaign exists
    existing = await ServiceCampaign.find_one({
        "platform_campaign_id": platform_campaign_id,
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
