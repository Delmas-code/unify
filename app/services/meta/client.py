import requests
from typing import Optional
from urllib.parse import urlencode

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

    def create_campaign(self, name: str, objective: str = "LINK_CLICKS"):
        data = {
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_categories": []
        }
        return self._post(f"act_{self.ad_account_id}/campaigns", data)

    def create_ad_set(self, campaign_id: str, **kwargs):
        data = {
            "campaign_id": campaign_id,
            "name": kwargs["name"],
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "LINK_CLICKS",
            "daily_budget": kwargs["daily_budget"],
            "start_time": kwargs["start_time"],
            "end_time": kwargs["end_time"],
            "status": "PAUSED",
            "targeting": kwargs["targeting"]
        }
        return self._post(f"act_{self.ad_account_id}/adsets", data)

    def create_ad_creative(self, name: str, page_id: str, message: str, link: str):
        data = {
            "name": name,
            "object_story_spec": {
                "page_id": page_id,
                "link_data": {
                    "message": message,
                    "link": link
                }
            }
        }
        return self._post(f"act_{self.ad_account_id}/adcreatives", data)

    def create_ad(self, name: str, ad_set_id: str, creative_id: str):
        data = {
            "name": name,
            "adset_id": ad_set_id,
            "creative": {"creative_id": creative_id},
            "status": "PAUSED"
        }
        return self._post(f"act_{self.ad_account_id}/ads", data)