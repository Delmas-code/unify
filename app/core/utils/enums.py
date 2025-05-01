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


class MetaBudgetType(str, Enum):
    DAILY = "daily"
    LIFETIME = "lifetime"
    
# class MetaCampaignObjective(str, Enum):
#     BRAND_AWARENESS = "BRAND_AWARENESS"
#     CONVERSIONS = "CONVERSIONS"
#     REACH = "REACH"
#     LINK_CLICKS = "LINK_CLICKS"
#     LANDING_PAGE_VIEWS = "LANDING_PAGE_VIEWS"
#     POST_ENGAGEMENT = "POST_ENGAGEMENT"
#     PAGE_LIKES = "PAGE_LIKES"
#     EVENT_RESPONSES = "EVENT_RESPONSES"
#     OFFER_CLAIMS = "OFFER_CLAIMS"
#     APP_INSTALLS = "APP_INSTALLS"
#     VIDEO_VIEWS = "VIDEO_VIEWS"
#     LEAD_GENERATION = "LEAD_GENERATION"
#     MESSAGES = "MESSAGES"
#     STORE_TRAFFIC = "STORE_TRAFFIC"
#     CATALOG_SALES = "CATALOG_SALES"

class MetaCampaignObjective(str, Enum):
    BRAND_AWARENESS = "BRAND_AWARENESS"
    CONVERSIONS = "CONVERSIONS"
    REACH = "REACH"
    LINK_CLICKS = "LINK_CLICKS"
    LANDING_PAGE_VIEWS = "LANDING_PAGE_VIEWS"
    POST_ENGAGEMENT = "POST_ENGAGEMENT"
    PAGE_LIKES = "PAGE_LIKES"
    APP_INSTALLS = "APP_INSTALLS"
    VIDEO_VIEWS = "VIDEO_VIEWS"
    MESSAGES = "MESSAGES"


class MetaBillingEvent(str, Enum):
    IMPRESSIONS = "IMPRESSIONS"
    LINK_CLICKS = "LINK_CLICKS"
    ACTIONS = "ACTIONS"
    
class MetaAdsetStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    INHERITED_FROM_SOURCE = "INHERITED_FROM_SOURCE"
    
class MetaAdCreativeType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    APP_INSTALL = "app_install"

