import requests
from typing import Optional
from urllib.parse import urlencode
from app.core.utils.enums import MetaAdsetStatus, CampaignStatus

from app.core.config import settings


class MetaAPIClient:
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = settings.META_BASE_URL

    def _url(self, endpoint: str):
        return f"{self.base_url}/{endpoint}"

    def _get(self, endpoint: str, params: dict = {}):
        params["access_token"] = self.access_token
        response = requests.get(self._url(endpoint), params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: dict):
        data["access_token"] = self.access_token
        response = requests.post(self._url(endpoint), data=data)
        response.raise_for_status()
        return response.json()

    def create_campaign(self, name: str, objective: str = "LINK_CLICKS", status: CampaignStatus = CampaignStatus.PAUSED):
        data = {
            "name": name,
            "objective": objective,
            "status": status,
            #"special_ad_categories": []
        }
        #maxadset per cmpaign
        return self._post(f"act_{self.ad_account_id}/campaigns", data)

    def create_ad_set(self, campaign_id: str, adset_data: dict):
        data = {
            "campaign_id": campaign_id,
            "name": adset_data["name"],
            "billing_event": adset_data["billing_event"],
            "optimization_goal": adset_data["optimization_goal"],
            "start_time": adset_data["start_time"],
            "end_time": adset_data["end_time"],
            "status": adset_data["status"],
            "targeting": adset_data["targeting"]
        }
        if ("budget_type" in adset_data) and (adset_data["budget_type"] == "daily"):
            data["daily_budget"]= adset_data["budget"]
        elif ("budget_type" in adset_data) and (adset_data["budget_type"] == "lifetime"):
            data["lifetime_budget"]= adset_data["budget"]
        else: return None
        return self._post(f"act_{self.ad_account_id}/adsets", data)
    

    def create_ad_creative(self, creative_data: dict):
        data = creative_data.copy()
        return self._post(f"act_{self.ad_account_id}/adcreatives", data)

    def create_ad(self, name: str, ad_set_id: str, creative_id: str, status: str = "PAUSED"):
        data = {
            "name": name,
            "adset_id": ad_set_id,
            "creative": {"creative_id": creative_id},
            "status": status
        }
        return self._post(f"act_{self.ad_account_id}/ads", data)
    
    
meta_client = MetaAPIClient(settings.META_USER_ACCESS_TOKEN, settings.META_AD_ACCOUNT_ID)