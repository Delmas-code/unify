from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from typing import List, Optional, Union, Literal
from app.core.utils.enums import MetaCampaignObjective, MetaBillingEvent

class MetaCampaignCreate(BaseModel):
    name: str
    objective: Literal["LINK_CLICKS", "CONVERSIONS", "APP_INSTALLS"] = "LINK_CLICKS"
    status: Literal["PAUSED", "ACTIVE"] = "PAUSED"

class MetaCampaign(BaseModel):
    # Mirror Meta's API fields: https://developers.facebook.com/docs/marketing-api/reference/campaign
    campaign_id: Optional[str]  # Populated after creation on Meta
    name: str
    objective: MetaCampaignObjective
    daily_budget: Optional[PositiveFloat]  # Meta-specific budget
    lifetime_budget: Optional[PositiveFloat]
    bid_strategy: Optional[str]
    status: str = "ACTIVE"

class MetaAdSet(BaseModel):
    # Ad Set fields (Meta-specific)
    targeting: dict  # Meta's targeting spec (age, location, interests)
    billing_event: MetaBillingEvent

class MetaAdCreative(BaseModel):
    # Ad Creative fields (image/video/carousel)
    creative_type: str
    image_hash: Optional[str]  # From Meta's image upload
    video_id: Optional[str]  # From Meta's video upload
    primary_text: str
    call_to_action: Optional[str]

class MetaAd(BaseModel):
    ad_name: str
    creative: MetaAdCreative
    ad_set: MetaAdSet


    