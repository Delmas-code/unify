from app.services.meta.schema import MetaCampaignCreate
from app.services.unified.schema import User
from app.core.utils.security import get_current_user

from app.services.meta.controller import create_meta_campaign
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/meta/service-campaign/", status_code=201, tags=["Meta"])
async def create_meta_service_campaign(
    campaign_data: MetaCampaignCreate,
    platform_campaign_id: str,
    current_user: User = Depends(get_current_user),
):
    campaign, db_status = create_meta_campaign(campaign_data, platform_campaign_id, current_user)
    if not db_status:
        return {
                "message": "Service campaign was created successfully but failed to create service campaign in the database",
                "data": campaign
            }    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create service campaign",
        )
    # Return the created campaign
    return {
            "message": "Service campaign was created successfully",
            "data": campaign
        }
