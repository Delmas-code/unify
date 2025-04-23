from datetime import datetime, timezone
from enum import Enum
from beanie import Document
from pydantic import BaseModel, Field, NonNegativeFloat, PositiveInt
from typing import List, Optional, Union, Literal
from app.core.utils.enums import MetaCampaignObjective, MetaBillingEvent, CampaignStatus, MetaObjectives

class MetaCampaignCreate(Document):
    name: str
    # objective: Literal["LINK_CLICKS", "CONVERSIONS", "APP_INSTALLS"] = "LINK_CLICKS"
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
        name = "meta_campaigns"

class MetaAdSet(BaseModel):
    # Ad Set fields (Meta-specific)
    targeting: dict  # Meta's targeting spec (age, location, interests)
    billing_event: MetaBillingEvent

class MetaAdSet(Document):
    campaign_id: str  # Foreign key to MetaCampaign
    name: str
    adset_id: Optional[str]  # ID returned from Meta
    budget: NonNegativeFloat
    optimization_goal: str
    billing_event: str
    targeting: dict  # Store Meta targeting structure
    start_time: datetime
    end_time: Optional[datetime]
    status: str = "PAUSED"
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


    