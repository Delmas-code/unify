from app.core.utils.loggers import setup_logger
from app.core.utils.enums import ServiceType, MetaBudgetType, MetaAdCreativeType
from app.services.unified.schema import PlatformCampaign
from app.services.meta.schema import MetaAdSet, MetaAdCreativeCreate, MetaAdCreative, MetaCampaign, MetaAd

from app.core.utils.helper import parse_object_id

logger = setup_logger("meta/handler", "logs/meta.log")


async def get_platform_campaign_from_adset(adset_id: str):
    adset_id = parse_object_id(adset_id)
    if not adset_id:
        logger.warning(f"Invalid adset id: {adset_id}")
        return None, "error", "Invalid adset id."
    
    adset = await MetaAdSet.find_one(MetaAdSet.id == adset_id)
    if not adset:
        logger.info(f"Adset with id: {adset_id} not found.")
        return None, "not_found", "Adset not found."

    meta_campaign_id = parse_object_id(adset.service_campaign_id)
    if not meta_campaign_id:
        logger.warning(f"Invalid Meta Campign id: {meta_campaign_id}")
        return None, "error", "Invalid meta campaign id."
    
    meta_campaign = await MetaCampaign.get(meta_campaign_id)
    if not meta_campaign:
        logger.info(f"Meta campaign with id: {meta_campaign_id} not found.")
        return None, "not_found", "Meta campaign not found."

    platform_campaign_id = parse_object_id(meta_campaign.platform_campaign_id)
    if not platform_campaign_id:
        logger.warning(f"Invalid Platform Campign id: {platform_campaign_id}")
        return None, "error", "Invalid platform campaign id."
    
    platform_campaign = await PlatformCampaign.get(platform_campaign_id)
    if not platform_campaign:
        logger.info(f"Platform campaign with id: {platform_campaign_id} not found.")
        return None, "not_found", "Platform campaign not found."
        # raise ValueError("PlatformCampaign not found.")

    return platform_campaign, "success", "Platform campaign found."


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
    
async def create_meta_service_adset(adset_data, service_campaign_id):
    try:
        if "daily_budget" in adset_data:
            budget = adset_data["daily_budget"]
            budget_type = MetaBudgetType.DAILY
        elif "lifetime_budget" in adset_data:
            budget = adset_data["lifetime_budget"]
            budget_type = MetaBudgetType.LIFETIME
        else:
            logger.error(f"Error no budget for `daily_budget` or `lifetime_budget` were found in {adset_data}")
            return None
        
        adset = MetaAdSet(
            campaign_id=str(service_campaign_id),
            name=adset_data["name"],
            adset_id= adset_data["id"],
            budget= budget,
            budget_type=budget_type,
            bid_amount= adset_data["bid_amount"],
            optimization_goal=adset_data["optimization_goal"],
            billing_event=adset_data["billing_event"],
            targeting=adset_data["targeting"],
            start_time=adset_data["start_time"],
            end_time=adset_data.get("end_time"),
            status=adset_data["status"]
        )
        await MetaAdSet.insert()
        logger.info(f"Meta adset created: {adset.id}")
        return adset
    except Exception as e:
        logger.error(f"Error creating meta adset with data -> {adset_data}: {e}")
        return None
    
def generate_ad_creative_payload(creative: MetaAdCreativeCreate) -> dict:
    try:
        base_payload = {
            "name": creative.name,
            "object_story_spec": {
                "page_id": creative.page_id
            }
        }

        if creative.creative_type == MetaAdCreativeType.IMAGE:
            base_payload["object_story_spec"]["link_data"] = {
                "message": creative.message,
                "link": creative.link_url,
                "image_url": creative.image_url,
                "call_to_action": {
                    "type": creative.call_to_action
                }
            }
        elif creative.creative_type == MetaAdCreativeType.VIDEO:
            base_payload["object_story_spec"]["video_data"] = {
                "video_id": creative.video_id,
                "message": creative.message,
                "call_to_action": {
                    "type": creative.call_to_action
                }
            }
        elif creative.creative_type == MetaAdCreativeType.APP_INSTALL:
            base_payload["object_story_spec"]["link_data"] = {
                "link": creative.app_store_link,
                "message": creative.message,
                "call_to_action": {
                    "type": "INSTALL_MOBILE_APP"
                }
            }
    except Exception as e:
        logger.error(f"Error generating ad creative payload: {e}")
        return None
    
    logger.info(f"Meta ad creative payload generated: {base_payload}")
    return base_payload

async def create_meta_service_ad_creative(creative_data: MetaAdCreativeCreate):
    try:
        # creative = MetaAdCreative(
        #     name=creative_data.name,
        #     creative_type=creative_data.creative_type,
        #     page_id=creative_data.page_id,
        #     message=creative_data.message,
        #     image_url=creative_data.image_url,
        #     video_id=creative_data.video_id,
        #     app_store_link=creative_data.app_store_link,
        #     link_url=creative_data.link_url,
        #     call_to_action=creative_data.call_to_action
        # )
        creative = MetaAdCreative(
            **creative_data.model_dump(exclude_unset=True)
        )
        await creative.insert()
        logger.info(f"Meta ad creative created in db successfully: {creative.id}")
        return creative
    except Exception as e:
        logger.error(f"Error creating meta ad creative in db: {e}")
        return None
    

async def create_meta_service_ad(meta_ad, creative_id, adset_id ):
    try:
        ad = MetaAd(
            adset_id= adset_id,
            name= meta_ad.name,
            ad_id= meta_ad.id,
            creative_id= creative_id,
            status= meta_ad.status
        )
        await ad.insert()
        logger.info(f"Meta ad created in db successfully: {ad.id}") 
        return ad
    except Exception as e:
        logger.error(f"Error creating meta ad in db: {e}")
        return None