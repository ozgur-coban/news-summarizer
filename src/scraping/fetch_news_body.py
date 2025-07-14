import requests
import json
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class AAArticleBodyFetcher:
    BASE_URL = "https://www.aa.com.tr"

    def __init__(
        self,
        metadata_path,
        output_path,
        min_delay=1,
        max_retries=2,
        session_reset_every=20,
    ):
        self.metadata_path = metadata_path
        self.output_path = output_path
        self.min_delay = min_delay
        self.max_retries = max_retries
        self.df = None
        self.ua = UserAgent()
        self.session_reset_every = (
            session_reset_every  # Re-init session every N requests
        )

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
                paragraphs = [p.get_text(strip=True) for p in main.find_all("p")]
                filtered_paragraphs = [
                    p
                    for p in paragraphs
                    if "Abonelik için lütfen iletişime geçiniz" not in p
                    and "AA'nın WhatsApp kanallarına katılın" not in p
                ]
                headings = [h.get_text(strip=True) for h in main.find_all(["h3", "h4"])]
                full_text = "\n".join(headings + filtered_paragraphs)
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
                # Re-initialize session every N requests
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
                # Randomized jitter: between min_delay and min_delay * 3 seconds
                time.sleep(random.uniform(self.min_delay, self.min_delay * 3))
            session.close()
        print(f"Done! {n_success}/{n_total} articles downloaded.")


if __name__ == "__main__":
    import sys

    # Usage: python fetch_articles.py metadata.jsonl aa_full_articles_{start}_{end}.jsonl start end
    metadata_path = sys.argv[1]
    output_path = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    fetcher = AAArticleBodyFetcher(metadata_path, output_path)
    fetcher.run(start=start, end=end)
