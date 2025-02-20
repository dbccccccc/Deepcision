"""
API Manager Module

This module provides a centralized manager for handling different API integrations.
It maintains a registry of API instances and manages their configurations.
"""

from typing import Dict, Optional

from api_integration.api_abstract import APIBase, ApiConfig
from api_integration.openrouter_api import OpenRouterAPI, OpenRouterConfig
from utils.config_loader import ConfigLoader


class ApiManager:
    """
    A singleton manager class that handles registration and access to different API integrations.
    
    Attributes:
        apis (Dict[str, APIBase]): Dictionary storing API instances with their names as keys
    """
    apis: Dict[str, APIBase] = {}

    def __init__(self):
        """Initialize an empty API manager"""
        pass

    def add_api(self, api: APIBase):
        """
        Register a new API instance in the manager
        
        Args:
            api (APIBase): The API instance to register
        """
        self.apis[api.api_name] = api

    def get_api(self, key: str) -> Optional[APIBase]:
        """
        Retrieve an API instance by its name
        
        Args:
            key (str): The name of the API to retrieve
            
        Returns:
            Optional[APIBase]: The requested API instance if found, None otherwise
        """
        return self.apis[key]

    def get_config(self, config: ConfigLoader, name: str) -> ApiConfig:
        """
        Get API configuration from the config loader
        
        Args:
            config (ConfigLoader): Configuration loader instance
            name (str): Name of the API configuration to load
            
        Returns:
            ApiConfig: Configuration for the specified API, or empty config if not found
        """
        if name == "openrouter":
            # Special handling for OpenRouter config
            raw_config = config.get_config(name) or {}
            return OpenRouterConfig(
                base_url=raw_config.get("base_url"),
                api_key=raw_config.get("api_key"),
                model=raw_config.get("model"),
                timeout=raw_config.get("timeout"),
                http_referer=raw_config.get("http_referer"),
                x_title=raw_config.get("x_title")
            )
        return config.get_config(name) or ApiConfig()

    def initialize(self, config: ConfigLoader) -> bool:
        """
        Initialize all supported APIs with their configurations
        
        Args:
            config (ConfigLoader): Configuration loader instance
            
        Returns:
            bool: True if initialization was successful
        """
        self.add_api(OpenRouterAPI(self.get_config(config, "openrouter")))
        return True
