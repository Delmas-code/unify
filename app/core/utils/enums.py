from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    ADVERTISER = "advertiser"  


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    CAMPAIGN_BUDGET = "campaign_budget"  # Deducted when campaigns are created


class ServiceType(str, Enum):
    META = "meta"
    GOOGLE = "google"
    TIKTOK = "tiktok"


class ServiceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"

class WalletCurrency(str, Enum):
    USD = "usd"
    CFA = "cfa"
    EURO = "euro"
    GBP = "gbp"


class MetaCampaignObjective(str, Enum):
    BRAND_AWARENESS = "BRAND_AWARENESS"
    CONVERSIONS = "CONVERSIONS"
    REACH = "REACH"


class MetaBillingEvent(str, Enum):
    IMPRESSIONS = "IMPRESSIONS"
    LINK_CLICKS = "LINK_CLICKS"
