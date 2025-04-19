import httpx

class MetaAdsClient:
    BASE_URL = "https://graph.facebook.com/v17.0"

    def __init__(self, access_token: str = None):
        self.access_token = access_token

    async def create_campaign(self, ad_account_id: str, name: str, objective: str, budget: int):
        url = f"{self.BASE_URL}/act_{ad_account_id}/campaigns"
        params = {
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_categories": [],
            "daily_budget": budget,
            "access_token": self.access_token
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=params)
            response.raise_for_status()
            return response.json()

    async def get_campaign(self, campaign_id: str):
        url = f"{self.BASE_URL}/{campaign_id}"
        params = {"access_token": self.access_token}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
