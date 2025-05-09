from fastapi import HTTPException
# from app.services.unified.client import MetaAdsClient
from app.services.unified.handler import ( create_user, authenticate_user, create_campaign, get_all_campaigns, 
                                          get_campaign_by_id, get_user_by_id)
from app.core.utils.loggers import setup_logger

logger = setup_logger("unified/controller", "logs/unified.log")

async def create_user_account(user_data):
    try:
        user = await create_user(user_data)
        if not user:
            raise HTTPException(status_code=500, detail="User account creation failed")
        return str(user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def login_user_account(user_data):
    try:
        token_response, msg = await authenticate_user(user_data)
        if token_response is None:
            raise HTTPException(status_code=500, detail="An error occurred during authentication")
        elif token_response is False and msg == "authorization_error":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        elif token_response is False and msg == "not_found":
            raise HTTPException(status_code=401, detail="User not found")
        
        return token_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_user_account(current_user):
    try:
        user_id = str(current_user.id)
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found or invalid user ID")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#TODO: need to enforce wallet check before allocating budget to a platform campaign
async def create_platform_campaign(campaign_data, current_user):
    try:
        user_id = str(current_user.id)
        campaign = await create_campaign("platform", campaign_data, user_id)
        if campaign is None:
            raise HTTPException(status_code=500, detail="An error occured during creation of platform campaign")
        
        return campaign
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def all_user_platform_campaigns(current_user):
    try:
        user_id = str(current_user.id)
        campaigns = await get_all_campaigns("platform", user_id)
        if campaigns is False:
            raise HTTPException(status_code=404, detail="No campaigns found for this user")
        elif campaigns is None:
            raise HTTPException(status_code=500, detail="An error occurred while fetching campaigns")
        
        print(f"campaigns: {campaigns}")
        return campaigns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_platform_campaign_by_id(campaign_id, current_user):
    try:
        user_id = str(current_user.id)
        campaign, err_message, message = await get_campaign_by_id(campaign_id, user_id)

        if campaign is False and err_message == "not_found":
            raise HTTPException(status_code=404, detail="Campaign not found")
        elif campaign is False and err_message == "authorization_error":
            raise HTTPException(status_code=403, detail="Campaign not owned by this user")
        elif campaign is None and err_message == "error":
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching the campaign: {message}")
        
        print(f"campaign: {campaign}")
        return campaign
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

"""
async def create_ad_campaign(payload: AdCreateRequest) -> AdResponse:
    client = MetaAdsClient(access_token=payload.access_token)
    campaign = await client.create_campaign(
        ad_account_id=payload.ad_account_id,
        name=payload.name,
        objective=payload.objective,
        budget=payload.budget
    )
    return AdResponse(
        campaign_id=campaign["id"],
        name=campaign["name"],
        status=campaign["status"],
        objective=campaign["objective"]
    )

async def get_ad_campaign(campaign_id: str) -> AdResponse:
    client = MetaAdsClient()
    campaign = await client.get_campaign(campaign_id)
    return AdResponse(
        campaign_id=campaign["id"],
        name=campaign["name"],
        status=campaign["status"],
        objective=campaign["objective"]
    )

    """