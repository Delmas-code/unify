import requests
from typing import Optional
from urllib.parse import urlencode
from app.core.utils.enums import MetaAdsetStatus, CampaignStatus

# from facebook_business.adobjects.campaign import Campaign
# from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects import campaign, adset, adcreative, ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi

from app.core.config import settings


class MetaAPIClient:
    def __init__(self, access_token: str, ad_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = settings.META_BASE_URL

        FacebookAdsApi.init(
            access_token=access_token,
            api_version='v22.0'  # Use latest stable version
        )

        self.account = AdAccount(f'act_{self.ad_account_id}')

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
        print(f"response Json {response.json()}\n response: {response}\n")
        return response.json()

    def create_campaign(self, name: str, objective: str = "LINK_CLICKS", status: CampaignStatus = CampaignStatus.PAUSED):
        try:
            meta_campaign = self.account.create_campaign(
                fields=[campaign.Campaign.Field.name, campaign.Campaign.Field.objective, campaign.Campaign.Field.status],
                params={
                    'name': name,
                    'objective': objective,
                    'status': status,
                    'special_ad_categories': [],
                }
            )
            return meta_campaign
        except Exception as e:
            print(f"Error creating campaign: {e}")
            return None
        #maxadset per cmpaign is 200

    def create_ad_set(self, campaign_id: str, adset_data: dict):
        try:
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

            meta_adset = self.account.create_ad_set(
                fields=[adset.AdSet.Field.name, adset.AdSet.Field.billing_event, adset.AdSet.Field.optimization_goal,
                        adset.AdSet.Field.start_time, adset.AdSet.Field.end_time, adset.AdSet.Field.status,
                        adset.AdSet.Field.targeting, adset.AdSet.Field.campaign_id],
                params= data
            )
            return meta_adset
        except Exception as e:
            print(f"Error creating adset: {e}")
            return None

    

    def create_ad_creative(self, creative_data: dict):
        try:
            data = creative_data.copy()
            meta_creative = self.account.create_ad_creative(
                # fields= [],
                params= data
            )
            return meta_creative
        except Exception as e:
            print(f"Error creating creative: {e}")
            return None

    def create_ad(self, name: str, ad_set_id: str, creative_id: str, status: str = "PAUSED"):
        try:
            data = {
                "name": name,
                "adset_id": ad_set_id,
                "creative": {"creative_id": creative_id},
                "status": status
            }
            meta_ad = self.account.create_ad(
                fields= [ad.Ad.Field.name, ad.Ad.Field.adset_id,
                         ad.Ad.Field.creative, ad.Ad.Field.status],
                params=data
            )
            return meta_ad
        except Exception as e:
            print(f"Error creating adset: {e}")
            return None
    
    
meta_client = MetaAPIClient(settings.META_USER_ACCESS_TOKEN, settings.META_AD_ACCOUNT_ID)