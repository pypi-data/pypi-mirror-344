import httpx
import os

class SKOpenAPIClient:
    BASE_URL = "https://apis.openapi.sk.com/puzzle"

    def __init__(self, app_key: str = None):
        self.app_key = app_key or os.getenv("APP_KEY")
        if not self.app_key:
            raise ValueError("APP_KEY environment variable is not set")
        self.client = httpx.Client(base_url=self.BASE_URL, headers={
            "accept": "application/json",
            "appKey": self.app_key
        })

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        merged_headers = self.client.headers.copy()
        if headers:
            merged_headers.update(headers)
        response = self.client.get(endpoint, params=params, headers=merged_headers)
        response.raise_for_status()
        return response 