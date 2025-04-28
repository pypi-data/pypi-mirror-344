from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchResult:
    """
    Represents a search result from the Bibly API."""
    doi: Optional[str]
    title: Optional[str]
    abstract: Optional[str]
    authors: Optional[str]
    date: Optional[str]
    source: Optional[str]
