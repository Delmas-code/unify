from pydantic import BaseModel, EmailStr, PositiveFloat
from beanie import Document
from datetime import datetime, timezone
from typing import List, Optional
from app.core.utils.enums import UserRole, TransactionType, ServiceType, ServiceStatus, CampaignStatus

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class User(Document):
    full_name: str
    username: str
    role: UserRole = UserRole.ADVERTISER
    email: EmailStr
    password: str
    # wallet: "Wallet"  # 1:1 relationship
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "users" #collection name in db

class Wallet(Document):
    user_id: str
    balance: PositiveFloat = 0.0  
    currency: str = "USD"
    updated_at: datetime

class Transaction(Document):
    id: str
    user_id: str
    amount: PositiveFloat
    type: TransactionType
    description: Optional[str]
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "transactions"

class ServiceCampaign(Document):
    id: str
    platform_campaign_id: str  # Links to PlatformCampaign
    service_type: ServiceType
    service_campaign: Optional[Document]  # Populated after creation on respective platform
    service_id: str  # ID from the respective platform (Meta, Google, TikTok)
    service_budget: PositiveFloat  # Portion of total_budget allocated to this service
    status: ServiceStatus = ServiceStatus.INACTIVE
    created_at: datetime = datetime.now(timezone.utc)

class PlatformCampaignBase(Document):
    name: str
    user_id: str 
    total_budget: PositiveFloat
    status: CampaignStatus = CampaignStatus.DRAFT
    start_date: Optional[datetime]
    end_date: Optional[datetime]

class PlatformCampaignCreate(PlatformCampaignBase):
    pass

class PlatformCampaign(PlatformCampaignBase):
    id: str
    created_at: datetime = datetime.now(timezone.utc)
    service_campaigns: List["ServiceCampaign"]  # Linked to Meta/Google/TikTok campaigns