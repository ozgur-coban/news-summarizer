import requests
from bs4 import BeautifulSoup


class AA_NewsFetcher:
    BASE_URL = "https://www.aa.com.tr/tr/Search"
    SEARCH_API_URL = "https://www.aa.com.tr/tr/Search/Search"

    def __init__(self, start_page=1, max_pages=1, category_id=2, keyword=""):
        self.start_page = start_page
        self.max_pages = max_pages
        self.category_id = category_id
        self.keyword = keyword
        self.results = []

    def _get_session_and_token(self):
        s = requests.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0"})
        r = s.get(self.BASE_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_input = soup.find("input", {"name": "__RequestVerificationToken"})
        csrf_token = token_input["value"] if token_input else None
        if not csrf_token:
            raise Exception("No CSRF token found")
        return s, csrf_token

    def _fetch_batch(self, session, csrf_token, page):
        data = {
            "PageSize": 20,
            "Page": page,
            "Keywords": self.keyword,
            "CategoryId": self.category_id,
            "TypeId": 1,
            "__RequestVerificationToken": csrf_token,
        }
        resp = session.post(self.SEARCH_API_URL, data=data, timeout=15)
        print(f"Status: {resp.status_code} (page {page})")
        resp.raise_for_status()
        return resp.json()

    def run(self):
        session, csrf_token = self._get_session_and_token()
        self.results.clear()
        for i in range(self.max_pages):
            page = self.start_page + i
            try:
                result = self._fetch_batch(session, csrf_token, page)
                docs = result.get("Documents", [])
                for doc in docs:
                    print(doc)
                    title = doc.get("Title")
                    link = "https://www.aa.com.tr" + doc.get("Route", "")
                    self.results.append((title, link))
                print(f"Fetched {len(docs)} articles on page {page}.")
            except Exception as e:
                print(f"Error fetching page {page}:", e)
                break
