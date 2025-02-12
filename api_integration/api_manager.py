
from typing import Dict, Optional

from api_integration.api_abstract import APIBase, ApiConfig
from api_integration.deepseek_api import DeepSeekAPI
from utils.config_loader import ConfigLoader


class ApiManager:
    apis: Dict[str, APIBase] = {}

    def __init__(self):
        pass

    def add_api(self, api: APIBase):
        self.apis[api.api_name] = api

    def get_api(self, key: str) -> Optional[APIBase]:
        return self.apis[key]

    def get_config(self, config: ConfigLoader, name: str) -> ApiConfig:
        return config.get_config(name) or ApiConfig()

    def initialize(self, config: ConfigLoader) -> bool:
        self.add_api(DeepSeekAPI(self.get_config(config, "deepseek")))
        return True
