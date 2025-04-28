from typing import Optional
from sprynger import init, Meta

from bibly.search_handler import SearchHandler
from bibly.utils.data_types import SearchResult

class SpringerHandler(SearchHandler):
    def initialize(self):
        """
        Initialize the Springer search handler with API key.
        """
        init(api_key = self.api_key)

    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the Springer API."""
        query += f" AND datefrom:{year_from}-01-01" if year_from else ""
        query += f" AND dateto:{year_to}-12-31" if year_to else ""

        springer_search = Meta(query, nr_results=100)

        results = []
        for entry in springer_search:
            creators = '; '.join([c.creator for c in entry.creators])
            results.append(
                SearchResult(
                    doi=entry.doi,
                    title=entry.title,
                    abstract=entry.abstract,
                    authors=creators,
                    date=entry.publicationDate,
                    source="Springer"
                )
            )
        return results

    def __init__(self, api_key: str):
        """
        Initialize the Springer search handler with API key.

        :param api_key: Springer API key
        """
        self.api_key = api_key
        self.initialize()
