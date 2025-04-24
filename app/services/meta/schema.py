from datetime import datetime, timezone
from beanie import Document
from pydantic import BaseModel, Field, NonNegativeFloat, HttpUrl
from typing import Optional
from app.core.utils.enums import (MetaCampaignObjective, MetaBillingEvent, ServiceType,
                                  CampaignStatus, MetaAdsetStatus, MetaBudgetType,
                                  MetaAdCreativeType)

class MetaCampaignCreate(Document):
    name: str
    objective: MetaCampaignObjective = MetaCampaignObjective.LINK_CLICKS
    status: CampaignStatus = CampaignStatus.PAUSED

class MetaCampaign(Document):
    # Mirror Meta's API fields: https://developers.facebook.com/docs/marketing-api/reference/campaign
    campaign_id: Optional[str]  # Populated after creation on Meta
    platform_campaign_id: str 
    service_type: ServiceType = ServiceType.META
    name: str
    objective: MetaCampaignObjective
    bid_strategy: Optional[str]
    status: CampaignStatus = CampaignStatus.PAUSED
    created_at: datetime = datetime.now(timezone.utc)
    
    class Settings:
        name = "service_campaigns"

class MetaAdSet(Document):
    campaign_id: str  # Foreign key to MetaCampaign
    name: str
    adset_id: Optional[str]  # ID returned from Meta
    budget: NonNegativeFloat
    budget_type: MetaBudgetType
    bid_amount: str # still to fully understand its use
    optimization_goal: MetaCampaignObjective
    billing_event: MetaBillingEvent
    targeting: dict  # Store Meta targeting structure
    start_time: datetime
    end_time: Optional[datetime] = 0
    service_type: ServiceType = ServiceType.META
    service_campaign_id: str 
    status: MetaAdsetStatus = MetaAdsetStatus.PAUSED
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "service_adsets"


class MetaAdCreativeBase(Document):
    name: str
    creative_type: MetaAdCreativeType
    page_id: str
    message: Optional[str] = None
    link_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    video_id: Optional[str] = None
    app_store_link: Optional[HttpUrl] = None
    call_to_action: Optional[str] = "LEARN_MORE"  # based on Meta CTA list

class MetaAdCreativeCreate(MetaAdCreativeBase):
    pass

class MetaAdCreative(MetaAdCreativeBase, Document):
    # platform_campaign_id: str
    # service_campaign_id: str
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "service_ad_creatives"


class MetaAd(Document):
    adset_id: str  # Foreign key to AdSet
    name: str
    ad_id: Optional[str]  # ID returned from Meta
    creative_id: str
    status: MetaAdsetStatus = MetaAdsetStatus.PAUSED
    service_type: ServiceType = ServiceType.META
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "service_ads"


