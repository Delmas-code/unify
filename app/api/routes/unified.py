from fastapi import APIRouter, HTTPException, Depends
from app.core.utils.security import get_current_user
from app.services.unified.schema import User, LoginRequest, PlatformCampaignCreate
from app.services.unified.controller import (create_user_account, login_user_account, create_platform_campaign
                                             )

router = APIRouter()

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
    
@router.post("/campaigns/platform/create", status_code=201, tags=["campaigns"])
async def add_platform_campaign(payload: PlatformCampaignCreate, current_user: User = Depends(get_current_user)):
    try:
        campaign = await create_platform_campaign(payload, current_user)
        return {
            "message": "Platform Campaign created successfully",
            "data": campaign
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))