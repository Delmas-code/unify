from app.services.meta.schema import MetaCampaignCreate, MetaAdSet, MetaAd
from app.services.unified.schema import User
from app.core.utils.security import get_current_user

from app.services.meta.controller import create_meta_campaign, create_meta_adset,create_meta_ad
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/service-campaign/create", status_code=201)
async def create_meta_service_campaign_route(
    campaign_data: MetaCampaignCreate,
    current_user: User = Depends(get_current_user),
):
    try:
        campaign, db_status = create_meta_campaign(campaign_data, current_user)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/adsets/create", status_code=201)
async def create_adset_route(
    service_campaign_id: str,
    adset_data: MetaAdSet,
    current_user: User = Depends(get_current_user)
):
    try:
        adset, db_status = create_meta_adset(service_campaign_id, adset_data, current_user)
        if not db_status:
            return {
                    "message": "Adset was created successfully but failed to create adset in the database",
                    "data": adset
                }    
        if not adset:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create adset",
            )
        # Return the created campaign
        return {
                "message": "Adset was created successfully",
                "data": adset
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ads/create", status_code=201)
async def create_meta_ad_route(
    # platform_campaign_id: str,
    ad_data: MetaAd,
    current_user: User = Depends(get_current_user)
):
    try:
        ad, db_status = create_meta_ad(ad_data, current_user)
        if not db_status:
            return {
                    "message": "Ad was created successfully but failed to create adset in the database",
                    "data": ad
                }    
        if not ad:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create ad",
            )
        # Return the created campaign
        return {
                "message": "Ad was created successfully",
                "data": ad
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
