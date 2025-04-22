from fastapi import APIRouter, HTTPException, Depends
from app.core.utils.security import get_current_user
from app.services.unified.schema import User, LoginRequest, PlatformCampaignCreate
from app.services.unified.controller import (create_user_account, login_user_account, create_platform_campaign,
                                             all_user_platform_campaigns, get_platform_campaign_by_id, 
                                             get_user_account
                                             )
from app.core.utils.loggers import setup_logger

router = APIRouter()
logger = setup_logger("routes/unified", "logs/routes_unified.log")

@router.get("/user", status_code=200, tags=["User"])
async def get_user(current_user: User = Depends(get_current_user)):
    try:
        user = await get_user_account(current_user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "message": "User account fetched successfully",
            "data": user
        }
    
    except Exception as e:
        logger.error(f"Error fetching user account: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user/register", status_code=201, tags=["User"])
async def register(payload: User):
    try:
        user_id = await create_user_account(payload)
        if not user_id:
            raise HTTPException(status_code=400, detail="User account creation failed")
        return {"message": "User account created successfully", "data": user_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/user/login", status_code=200, tags=["User"])
async def login(payload: LoginRequest):
    try:
        token_response = await login_user_account(payload)
        if not token_response:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful", "data": token_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/campaign/platform/create", status_code=201, tags=["campaigns"])
async def add_platform_campaign(payload: PlatformCampaignCreate, current_user: User = Depends(get_current_user)):
    try:
        campaign = await create_platform_campaign(payload, current_user)
        return {
            "message": "Platform Campaign created successfully",
            "data": campaign
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/campaign/platform/all", status_code=200, tags=["campaigns"])
async def get_all_platform_campaigns(current_user: User = Depends(get_current_user)):
    try:
        campaigns = await all_user_platform_campaigns(current_user)
        return {
            "message": "Platform Campaigns fetched successfully",
            "data": campaigns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/campaign/platform/single", status_code=200, tags=["campaigns"])
async def get_platform_campaign(
    campaign_id: str, 
    current_user: User = Depends(get_current_user)
):
    try:
        campaign = await get_platform_campaign_by_id(campaign_id, current_user)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {
            "message": "Platform Campaign fetched successfully",
            "data": campaign
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))