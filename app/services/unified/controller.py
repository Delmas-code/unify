from fastapi import HTTPException
# from app.services.unified.client import MetaAdsClient
from app.services.unified.handler import create_user, authenticate_user


async def create_user_account(user_data):
    user = await create_user(user_data)
    if not user:
        raise HTTPException(status_code=400, detail="User account creation failed")
    return str(user.id)

async def login_user_account(user_data):
    token_response = await authenticate_user(user_data)
    if token_response is None:
        raise HTTPException(status_code=500, detail="An error occurred during authentication")
    elif token_response is False:
        raise HTTPException(status_code=500, detail="Invalid credentials")
    
    return token_response


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