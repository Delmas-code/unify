from app.core.utils.loggers import setup_logger
from app.core.utils.enums import ServiceType, MetaBudgetType
from app.services.unified.schema import PlatformCampaign
from app.services.meta.schema import MetaAdSet

logger = setup_logger("meta/handler", "logs/meta.log")

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