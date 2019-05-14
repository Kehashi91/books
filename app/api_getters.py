from pydash.objects import get
import requests


BASE_URL = "https://www.googleapis.com/books/v1/volumes?" \
           "q={}" \
           "&maxResults=40" \
           "&startIndex={}" \
           "&fields=totalItems,items(id,volumeInfo(title,authors,categories,description))"


class BulkSearch:
    """Allow for searching all the results from book API. It requires traversing the API pagination with multiple
    requests.
    """
    def __init__(self, max_results=1000):
        self.max_results = max_results
        self.current_result = 0
        self.session = requests.Session()  # use persitent session

    def search_bulk(self, keywords=None, author=None):
        """Build a list of all books for given author/keyword combination"""
        rv = list()

        if not keywords and not author:
            raise KeyError("No value for search!")

        while self.current_result <= self.max_results:
            r = self.search_books(keywords=keywords, author=author, index=self.current_result)
            if get(r, 'items'):
                for book in r['items']:
                    rv.append(book)
                    self.current_result += 1
            else:
                return rv  # as there are no more results, we exit the while loop
        return rv

    def search_books(self, keywords=None, author=None, index=1):
        """
        Builds the url and sends the request
        """
        query_params = list()

        if keywords:
            query_params.append(keywords)
        if author:
            query_params.append(f"inauthor:{author}")
        query_params = "+".join(query_params)
        r = self.session.get(BASE_URL.format(query_params, index)).json()

        return r
