from abc import ABC, abstractmethod
from typing import Optional

from bibly.utils.data_types import SearchResult


class SearchHandler(ABC):
    """Abstract base class for search handlers."""
    @abstractmethod
    def initialize(self):
        """Initialize the search handler."""
        pass

    @abstractmethod
    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """Search for a given query."""
        pass
