import requests

BASE_URL = "https://www.googleapis.com/books/v1/volumes?q={}&fields=totalItems,items(id,volumeInfo(title,authors,categories,description))"


def search_books(keywords=None, author=None):
    if not keywords and not author:
        raise KeyError("No value for search!")

    query_params = list()

    if keywords:
        query_params.append(keywords)
    if author:
        query_params.append(f"inauthor:{author}")

    query_params = "+".join(query_params)
    r = requests.get(BASE_URL.format(query_params))

    return r.json()
