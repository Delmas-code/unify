from fastapi import HTTPException
from app.core.utils.loggers import setup_logger

from app.services.unified.schema import PlatformCampaign, Wallet
from app.services.meta.schema import MetaCampaign
from app.core.utils.helper import parse_object_id, check_user_wallet_balance
from app.services.meta.handler import (create_meta_service_campaign, create_meta_service_adset, 
                                       generate_ad_creative_payload, create_meta_service_ad_creative,
                                       get_platform_campaign_from_adset, create_meta_service_ad)
from app.services.meta.client import meta_client

logger = setup_logger("meta/controller", "logs/meta.log")

async def create_meta_campaign(campaign_data, platform_campaign_id, current_user):
    try:
        #1: get platform campaign
        
        platform_campaign_id = parse_object_id(platform_campaign_id)

        if not platform_campaign_id:
            logger.warning(f"Invalid plaform campaign id: {platform_campaign_id}")
            raise HTTPException(status_code=400, detail="Invalid platform campaign id")

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
        service_campaign = meta_client.create_campaign(campaign_data["name"], campaign_data["objective"], campaign_data["status"])
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
        
async def create_meta_adset(service_campaign_id: str, adset_data: dict, current_user):
    try:
        service_campaign_id = parse_object_id(service_campaign_id)
        if not service_campaign_id:
            logger.warning(f"Invalid service campaign id: {service_campaign_id}")
            raise HTTPException(status_code=400, detail="Invalid service campaign id")

        service_campaign = await MetaCampaign.find_one(MetaCampaign.id == service_campaign_id)
        
        platform_campaign_id = parse_object_id(service_campaign.platform_campaign_id)
        if not platform_campaign_id:
            logger.warning(f"Invalid platform campaign id: {platform_campaign_id}")
            raise HTTPException(status_code=400, detail="Invalid service campaign id")
        
        platform_campaign = await PlatformCampaign.find_one({"_id": platform_campaign_id})
        if not platform_campaign:
                logger.warning(f"No platform campaign found with id: {platform_campaign_id}")
                raise HTTPException(status_code=404, detail="Platform campaign not found")

        user_id = str(current_user.id)
        if str(platform_campaign.user_id) != user_id:
            logger.warning(f"Campaign with id: {str(platform_campaign.id)} does not belong to user with id: {user_id}")
            raise HTTPException(status_code=403, detail="Campaign not owned by this user")
        
        #check user wallet to ensure they have enough balance to create the adset
        adset_budget =adset_data["budget"]
        wallet = await Wallet.find_one(Wallet.user_id == user_id)
        result = check_user_wallet_balance(wallet, adset_budget)
        if not result:
            logger.warning(f"User with id: {user_id} does not have enough balance to create adset with budget: {adset_budget}")
            raise HTTPException(status_code=400, detail="User does not have enough balance to create adset with budget")
        
        if not await platform_campaign.check_user_wallet(adset_budget):
            logger.warning(f"User with id: {user_id} does not have enough balance to create adset with budget: {adset_budget}")
            raise HTTPException(status_code=403, detail="User does not have enough balance to create adset")
        meta_ad_set = meta_client.create_ad_set(str(service_campaign_id), adset_data)
        if not meta_ad_set:
                logger.error(f"Failed to create adset on meta: {adset_data}")
                raise HTTPException(status_code=500, detail="Failed to create adset on meta")
        
        adset = create_meta_service_adset(meta_ad_set, service_campaign_id)
        if not adset:
            return meta_ad_set, False
            
        return adset, True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_meta_ad_creative(creative):
    try:
        creative_payload = generate_ad_creative_payload(creative)
        meta_creative = meta_client.create_ad_creative(creative_payload)
        if not meta_creative:
            logger.error(f"Failed to create ad creative on meta: {creative_payload}")
            raise HTTPException(status_code=500, detail="Failed to create ad creative on meta")
        ad_creative = await create_meta_service_ad_creative(meta_creative)
        if not ad_creative:
            return meta_creative, False
        return ad_creative, True
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def create_meta_ad(ad_data: dict, current_user):
    try:

        # Step 0: Get platform id and validate user
        platform_campaign, status, message = get_platform_campaign_from_adset(ad_data["adset_id"])
        if not platform_campaign and status == "not_found":
            raise HTTPException(status_code=404, detail=message)
        elif not platform_campaign and status == "error":
            raise HTTPException(status_code=400, detail=message)
        
        user_id = str(current_user.id)
        if str(platform_campaign.user_id) != user_id:
            logger.warning(f"Platform Campaign with id: {str(platform_campaign.id)} does not belong to user with id: {user_id}")
            raise HTTPException(status_code=403, detail="Campaign not owned by this user")

        # Step 1: Create Creative
        creative_id = await create_meta_ad_creative(ad_data["creative"])
        
        # Step 2: Create Ad using creative
        meta_ad = await meta_client.create_ad(ad_data["name"], ad_data["adset_id"], creative_id, ad_data["status"])
        if not meta_ad:
            logger.error(f"Failed to create ad on meta: {ad_data}")
            raise HTTPException(status_code=500, detail="Failed to create ad on meta")


        # Step 3: Save to DB
        ad = create_meta_service_ad(meta_ad, ad_data["adset_id"], creative_id)
        if not ad:
            return meta_ad, False
        return ad, True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
