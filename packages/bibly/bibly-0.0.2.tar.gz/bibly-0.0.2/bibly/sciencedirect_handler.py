from typing import Optional

from pybliometrics.sciencedirect import init, ScienceDirectSearch

from bibly.search_handler import SearchHandler
from bibly.utils.data_types import SearchResult


class SciencedirectHandler(SearchHandler):
    def initialize(self):
        """
        Initialize the Scopus search handler with API key and token.

        :param api_key: Scopus API key
        :param api_token: Scopus API token
        """
        if self.api_token:
            init(keys=[self.api_key], inst_tokens=[self.api_token])
        else:
            init(keys=[self.api_key])

    def search(self,
               query: str,
               year_from: Optional[str | int] = None,
               year_to: Optional[str | int] = None) -> list[SearchResult]:
        """ Search for a given query using the ScienceDirectSearch API."""
        query += f" AND DATE({year_from}-{year_to})" if year_from or year_to else ""

        sciencedirect_search = ScienceDirectSearch(query)

        results = []
        if sciencedirect_search.results:
            for entry in sciencedirect_search.results:
                results.append(
                    SearchResult(
                        doi=entry.doi,
                        title=entry.title,
                        abstract=None,
                        authors=entry.authors,
                        date=entry.coverDate,
                        source="ScienceDirect"
                    )
                )
        return results


    def __init__(self,
                 api_key: str,
                 api_token: Optional[str]):
        """
        Initialize the ScienceDirect search handler with API key and token.

        :param api_key: ScienceDirect API key
        :param api_token: ScienceDirect API token
        """
        self.api_key = api_key
        self.api_token = api_token
        self.initialize()
