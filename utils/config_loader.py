"""
Configuration Loading Utility
Responsible for loading and managing project configuration
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from ..architecture import Component

class ConfigLoader(Component):
    """Configuration Loader"""
    
    def __init__(self, config_path: str = "config"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.initialized: bool = False
    
    def initialize(self) -> bool:
        """Initialize configuration loader"""
        try:
            self._load_configs()
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
    
    def get_config(self, key: str) -> Optional[Any]:
        """Get configuration item"""
        return self.config.get(key)
    
    def _load_configs(self):
        """Load all configuration files"""
        if not self.config_path.exists():
            self.config_path.mkdir(parents=True)
        
        # Load JSON configuration
        for json_file in self.config_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                self.config.update(json.load(f))
        
        # Load YAML configuration
        for yaml_file in self.config_path.glob("*.yaml"):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                self.config.update(yaml.safe_load(f))
    
    def save_config(self, key: str, value: Any) -> bool:
        """Save configuration item"""
        try:
            self.config[key] = value
            # TODO: Implement configuration persistence
            return True
        except Exception:
            return False

# Example configuration file config.example.json
"""
{
    "api_keys": {
        "deepseek": "your_deepseek_key",
        "chatpdf": "your_chatpdf_key",
        "stirling": "your_stirling_key"
    },
    "system": {
        "max_threads": 5,
        "cache_ttl": 3600,
        "log_level": "info"
    }
}
""" 