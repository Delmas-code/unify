from pydantic import BaseModel, EmailStr, NonNegativeFloat, model_validator
from beanie import Document
from datetime import datetime, timezone
from typing import List, Optional
from app.core.utils.enums import UserRole, TransactionType, ServiceType, ServiceStatus, CampaignStatus, WalletCurrency

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    id: str | None = None
    email: str | None = None

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
    balance: NonNegativeFloat = 0.0  
    currency: WalletCurrency = WalletCurrency.USD
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "wallets"

class Transaction(Document):
    id: str
    user_id: str
    amount: NonNegativeFloat
    type: TransactionType
    description: Optional[str] = None
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "transactions"

class ServiceCampaign(Document):
    platform_campaign_id: str  # Links to PlatformCampaign
    service_type: ServiceType
    service_campaign: Optional[Document] = None  # Populated after creation on respective platform
    service_id: str  # ID from the respective platform (Meta, Google, TikTok)
    status: ServiceStatus = ServiceStatus.INACTIVE
    created_at: datetime = datetime.now(timezone.utc)

class PlatformCampaignBase(Document):
    name: str
    description: Optional[str] = None
    total_budget: NonNegativeFloat
    status: CampaignStatus = CampaignStatus.DRAFT
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_dates(self) -> "PlatformCampaignBase":
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")
        return self
    

class PlatformCampaignCreate(PlatformCampaignBase):
    pass

class PlatformCampaign(PlatformCampaignBase):
    user_id: str
    created_at: datetime = datetime.now(timezone.utc)
    # service_campaigns: List["ServiceCampaign"] = []  # Linked to Meta/Google/TikTok campaigns

    class Settings:
        name = "platform_campaigns"
