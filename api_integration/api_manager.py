"""
API Manager Module

This module provides a centralized manager for handling different API integrations.
It maintains a registry of API instances and manages their configurations.
"""

from typing import Dict, Optional

from api_integration.api_abstract import APIBase, ApiConfig
from api_integration.deepseek_api import DeepSeekAPI
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
        return config.get_config(name) or ApiConfig()

    def initialize(self, config: ConfigLoader) -> bool:
        """
        Initialize all supported APIs with their configurations
        
        Args:
            config (ConfigLoader): Configuration loader instance
            
        Returns:
            bool: True if initialization was successful
        """
        self.add_api(DeepSeekAPI(self.get_config(config, "deepseek")))
        return True
