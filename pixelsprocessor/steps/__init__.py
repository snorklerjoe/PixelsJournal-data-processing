"""Classes for loading and indexing the configuration

Pieces
- data
    - source
        - file
            a JSON file containing the data
    - filtering
        - query
            a query string to filter the data (SQL-like)
- processing
    Linearly executed processing steps that cascade into one another
    - type
        Parameter of the step
    - options (optional)
        Additional parameters of the step
    - export (optional)
        Export the data at this point to a CSV file
- output
    Data analysis output options
    - stats
        - catenum
            Enumeration of categories
        - onevar
            One-variable statistics
        - forecast
            Mood forecast
    - tables
        Tables to print or export
    - graphs
        Graphs to plot or export
        - timeline
            - show
"""

from abc import ABC, abstractmethod

class ConfigStep(ABC):
    """Abstract class for a configuration step."""

    def __init__(self, config: dict, context: ):
        """Initializes a ConfigStep object.

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
        """Runs the configuration step.
        """
        pass
