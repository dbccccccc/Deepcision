"""
Configuration Loading Utility
Responsible for loading and managing project configuration
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional

from api_integration.api_abstract import ApiConfig
from utils.architecture import Component


class ConfigLoader(Component):
    """Configuration Loader"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config: Dict[str, ApiConfig] = {}
        self.initialized: bool = False

    def initialize(self) -> bool:
        """Initialize configuration loader"""
        try:
            self.load_configs()
            self.initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize configuration loader: {str(e)}")
            return False

    def shutdown(self) -> bool:
        """Shutdown configuration loader"""
        try:
            self.config.clear()
            self.initialized = False
            return True
        except Exception:
            return False

    def get_config(self, key: str) -> Optional[ApiConfig]:
        """Get configuration item"""
        return self.config.get(key)

    def load_configs(self):
        """Load all configuration files"""
        if not self.config_file.exists():
            print(f"Failed to load config : {str(self.config_file)}")
            pass
        # Load JSON configuration
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config.update(json.load(f))

    def save_config(self, key: str, value: Any) -> bool:
        """Save configuration item"""
        try:
            self.config[key] = value
            if not self.config_file.exists():
                print(f"Failed to save config : {str(self.config_file)}")
                pass
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception:
            return False


# Example configuration file config.example.json
"""
{
    "deepseek":{
       "timeout":1000,
       "base_url":"xxxxx"
    }
}
"""
