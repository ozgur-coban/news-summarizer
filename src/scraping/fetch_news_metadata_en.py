import requests
import json
from bs4 import BeautifulSoup
# TODO merge with fetch_news_metadata_tr and make the url used based on parameter
# Url used + headers


class AA_EnglishNewsMetadataFetcher:
    BASE_URL = "https://www.aa.com.tr/en/Search"
    SEARCH_API_URL = "https://www.aa.com.tr/en/Search/Search"

    def __init__(
        self,
        start_page=1,
        max_pages=1,
        category_id=4,  # Example: 4 = "World" (change as needed)
        keyword="* * *",  # For ALL news use "* * *"
        save_to_file=False,
        save_file_path="",
        is_inplace=True,
        page_size=20,  # English endpoint allows up to 100
    ):
        self.start_page = start_page
        self.max_pages = max_pages
        self.category_id = category_id
        self.keyword = keyword
        self.results = []
        self.save_to_file = save_to_file
        self.save_file_path = save_file_path
        self.is_inplace = is_inplace
        self.page_size = page_size

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
            "PageSize": self.page_size,
            "Page": page,
            "Keywords": self.keyword,
            "CategoryId": self.category_id,
            "TypeId": 1,
            "__RequestVerificationToken": csrf_token,
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": self.BASE_URL,
            "Origin": "https://www.aa.com.tr",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        resp = session.post(self.SEARCH_API_URL, data=data, headers=headers, timeout=25)
        print(f"Status: {resp.status_code} (page {page})")
        resp.raise_for_status()
        return resp.json()

    def run(self):
        session, csrf_token = self._get_session_and_token()
        self.results.clear()
        file_mode = "w" if self.is_inplace else "a"
        file_path = self.save_file_path

        for i in range(self.max_pages):
            page = self.start_page + i
            try:
                result = self._fetch_batch(session, csrf_token, page)
                docs = result.get("Documents", [])
                for doc in docs:
                    title = doc.get("Title")
                    link = "https://www.aa.com.tr" + doc.get("Route", "")
                    self.results.append((title, link))
                print(f"Fetched {len(docs)} articles on page {page}.")
                if self.save_to_file:
                    with open(file_path, file_mode, encoding="utf-8") as f:
                        for doc in docs:
                            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
                file_mode = "a"  # After first write, always append
            except Exception as e:
                print(f"Error fetching page {page}:", e)
                break
