BibLy
=====
`BibLy` is a Python library designed to streamline academic literature searches by integrating multiple APIs (e.g., Scopus, Springer, ScienceDirect). It provides a unified interface for querying, filtering, and retrieving research articles, enabling efficient data collection and analysis for literature reviews.


⬇️ Install
-----------
Download and install the package from PyPI:

.. code-block:: bash

    pip install bibly


🪧 Example Use
---------------

.. code:: python

    >>> from bibly import BibLy
    >>> # Create client
    >>> client = BibLy(scopus_key=scopus_key, springer_key=springer_key)
    >>> # Search using two keywords
    >>> results = client.search(query="iab-bamf-soep AND integration",
                                year_from=2015,
                                year_to=2017)
    >>> # Print results
    >>> results
    [SearchResult(doi='10.1016/j.rssm.2021.100610', title='To work or to study? Postmig...'),
     SearchResult(doi='10.1016/j.rssm.2023.100842', title='Gender employment gap at arr...'),
     SearchResult(doi='10.1016/j.worlddev.2024.106833', title='Barriers to humanitarian...')]
