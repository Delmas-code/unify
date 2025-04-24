from datetime import datetime, timezone
from beanie import Document
from pydantic import BaseModel, Field, NonNegativeFloat, PositiveInt
from typing import Optional
from app.core.utils.enums import (MetaCampaignObjective, MetaBillingEvent, 
                                  CampaignStatus, MetaAdsetStatus, MetaBudgetType)

class MetaCampaignCreate(Document):
    name: str
    objective: MetaCampaignObjective = MetaCampaignObjective.LINK_CLICKS
    status: CampaignStatus = CampaignStatus.PAUSED

class MetaCampaign(Document):
    # Mirror Meta's API fields: https://developers.facebook.com/docs/marketing-api/reference/campaign
    campaign_id: Optional[str]  # Populated after creation on Meta
    platform_campaign_id: str 
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
    status: MetaAdsetStatus = MetaAdsetStatus.PAUSED
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "meta_ad_sets"

class Ad(Document):
    adset_id: str  # Foreign key to AdSet
    name: str
    ad_id: Optional[str]  # ID returned from Meta
    creative: dict  # Can store headline, image_url, description, etc.
    status: str = "PAUSED"
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "meta_ads"


    