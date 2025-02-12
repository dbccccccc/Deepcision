
from typing import Dict, Optional

from api_integration.api_abstract import APIBase


class ApiManager:
    apis: Dict[str, APIBase] = {}

    def __init__(self):
        pass

    def add_api(self, key: str, api: APIBase):
        self.apis[key] = api

    def get_api(self, key: str) -> Optional[APIBase]:
        return self.apis[key]
