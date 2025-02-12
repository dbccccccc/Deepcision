"""
Deepcision - Intelligent Decision System Architecture
This module defines the core architecture and component relationships of the project
"""
from abc import ABC, abstractmethod


class Component(ABC):
    """Abstract base class for all components"""

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize component"""
        pass

    @abstractmethod
    def shutdown(self) -> bool:
        """Shutdown component"""
        pass
