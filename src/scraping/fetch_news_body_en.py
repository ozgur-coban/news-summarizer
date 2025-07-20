import requests
import json
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# TODO merger with fetch_news_body_tr
# Url, parts is unnecessary


class AA_EnglishArticleBodyFetcher:
    BASE_URL = "https://www.aa.com.tr"

    def __init__(
        self,
        metadata_path,
        output_path,
        min_delay=0.01,
        max_retries=1,
        session_reset_every=20,
    ):
        self.metadata_path = metadata_path
        self.output_path = output_path
        self.min_delay = min_delay
        self.max_retries = max_retries
        self.df = None
        self.ua = UserAgent()
        self.session_reset_every = session_reset_every

    def load_metadata(self):
        if self.metadata_path.endswith(".jsonl"):
            self.df = pd.read_json(self.metadata_path, lines=True)
        elif self.metadata_path.endswith(".json"):
            self.df = pd.read_json(self.metadata_path)
        else:
            raise ValueError("Only .json or .jsonl files supported for AA metadata.")
        print(f"Loaded {len(self.df)} metadata rows.")

    def fetch_article_body(self, url, session, user_agent):
        tries = 0
        while tries < self.max_retries:
            try:
                headers = {"User-Agent": user_agent}
                resp = session.get(url, headers=headers, timeout=25)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                main = soup.find("div", class_="detay-icerik")
                if main is None:
                    return ""
                # Optionally get location/city (e.g. GENEVA) at the top
                parts = []

                # Subheadings
                headings = [h.get_text(strip=True) for h in main.find_all(["h3", "h4"])]

                # Main body paragraphs (ENGLISH: <p class="selectionShareable">)
                paragraphs = [
                    p.get_text(strip=True)
                    for p in main.find_all("p", class_="selectionShareable")
                ]

                # Filter out subscription/junk lines (ENGLISH ONLY)
                filtered_paragraphs = [
                    p
                    for p in paragraphs
                    if not (
                        "Anadolu Agency website contains only" in p
                        or "Please contact us for subscription options" in p
                    )
                ]
                # Compose full article
                full_text = "\n".join(parts + headings + filtered_paragraphs)
                if not full_text.strip():
                    return main.get_text(strip=True)
                return full_text
            except Exception as e:
                tries += 1
                print(f"Error fetching {url} (try {tries}/{self.max_retries}): {e}")
                time.sleep(random.uniform(self.min_delay, self.min_delay * 4))
        return ""

    def run(self, start=0, end=None, resume_file=None):
        if self.df is None:
            self.load_metadata()
        records = self.df.iloc[start:end].to_dict(orient="records")
        done_ids = set()
        if resume_file:
            try:
                with open(resume_file, encoding="utf-8") as f:
                    for line in f:
                        obj = json.loads(line)
                        done_ids.add(obj["Id"])
                print(f"Resuming: found {len(done_ids)} already downloaded articles.")
            except Exception:
                pass
        n_total = len(records)
        n_success = 0

        with open(self.output_path, "a", encoding="utf-8") as out:
            session = requests.Session()
            for i, item in enumerate(records):
                if i % self.session_reset_every == 0:
                    session.close()
                    session = requests.Session()

                user_agent = self.ua.random
                news_id = item.get("Id")
                title = item.get("Title")
                route = item.get("Route")
                if not route or not isinstance(route, str):
                    print(f"Skipping missing route: {news_id}")
                    continue
                if news_id in done_ids:
                    print(f"Already downloaded: {news_id}")
                    continue
                url = self.BASE_URL + route if route.startswith("/") else route

                text = self.fetch_article_body(url, session, user_agent)
                if not text or len(text) < 50:
                    print(f"Failed or empty article for {url}")
                else:
                    n_success += 1
                out_obj = {"Id": news_id, "Title": title, "Url": url, "full_text": text}
                out.write(json.dumps(out_obj, ensure_ascii=False) + "\n")
                print(
                    f"[{i + 1}/{n_total}] Downloaded Id {news_id} ({len(text)} chars)."
                )
                time.sleep(random.uniform(self.min_delay, self.min_delay * 3))
            session.close()
        print(f"Done! {n_success}/{n_total} articles downloaded.")
