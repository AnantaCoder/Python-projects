import requests

def get_book_info_with_cover(query):
    base_url = "https://archive.org/advancedsearch.php"
    params = {
        "q": query,
        "fl[]": ["identifier", "title", "creator", "year", "subject"],
        "output": "json",
        "rows": 10  # Adjust as needed
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    results = []
    for doc in data['response']['docs']:
        book_info = {
            "identifier": doc.get("identifier"),
            "title": doc.get("title"),
            "creator": doc.get("creator"),
            "year": doc.get("year"),
            "subject": doc.get("subject"),
            "cover_url": f"https://archive.org/services/img/{doc.get('identifier')}"
        }
        results.append(book_info)

    return results

# Example usage
query = "title:(pride and prejudice)"
books = get_book_info_with_cover(query)

for book in books:
    print(f"Title: {book['title']}")
    print(f"Cover URL: {book['cover_url']}")
    print("---")
