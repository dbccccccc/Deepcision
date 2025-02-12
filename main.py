"""
Deepcision Main Entry
"""
import asyncio
from typing import Dict, Any

from agents.role_manager import RoleManager
from api_integration.api_manager import ApiManager
from core.reasoning_engine import ReasoningEngine
from utils.config_loader import ConfigLoader


class Deepcision:
    """Deepcision Main Class"""

    def __init__(self):
        self._setup_components()

    def _setup_components(self):
        """Setup components"""
        self.api_manager = ApiManager()
        # Configuration loader
        self.config_loader = ConfigLoader()

        # Role manager
        self.role_manager = RoleManager()

        # Reasoning engine
        self.reasoning_engine = ReasoningEngine()

    async def initialize(self) -> bool:
        """Initialize system"""
        try:
            # Initialize components in sequence
            if not self.config_loader.initialize():
                return False

            if not self.role_manager.load_templates():
                return False

            if not self.reasoning_engine.initialize():
                return False

            return True
        except Exception as e:
            print(f"System initialization failed: {str(e)}")
            return False

    async def process_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Process query request"""
        try:
            # Use reasoning engine to process query
            result = await self.reasoning_engine.reason(query)
            return result or {"error": "Processing failed"}
        except Exception as e:
            return {"error": str(e)}

    async def shutdown(self):
        """Shutdown system"""
        try:
            self.reasoning_engine.shutdown()
            self.role_manager.terminate_all_agents()
            self.config_loader.shutdown()
        except Exception as e:
            print(f"Error during system shutdown: {str(e)}")


async def main():
    """Main function"""
    app = Deepcision()
    if await app.initialize():
        print("Deepcision system initialized successfully")
        # TODO: Add actual application logic
    else:
        print("Deepcision system initialization failed")

if __name__ == "__main__":
    asyncio.run(main())
