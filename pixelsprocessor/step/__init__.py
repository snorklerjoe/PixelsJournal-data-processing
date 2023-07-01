""" Classes that represent potential steps that can be called into procedure via configuration.
"""

from abc import ABC, abstractmethod
from pixelsprocessor.context import PixelProcessingContext as Context

class Step(ABC):
    """Abstract class for a procedure step."""

    def __init__(self, config: dict, context: Context):
        """Initializes a Step object.

        Args:
            config (dict): The configuration for the step.
        """
        self.config = config

    @abstractmethod
    def check(self) -> bool:
        """Checks if the configuration is valid.

        Returns:
            bool: True if the configuration is valid, False otherwise.
        """
        pass

    @abstractmethod
    def run(self):
        """Runs the step.
        """
        pass
