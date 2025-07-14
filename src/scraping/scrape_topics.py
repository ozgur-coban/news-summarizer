# TODO make sure that all of them are under detay-paylas exactly
import os
import pandas as pd
import re
from bs4 import BeautifulSoup
from preprocessing.text_preprocessor import TurkishNLTKPreprocessor


class TagExtractor:
    def __init__(self, html_dir: str, preprocessor: TurkishNLTKPreprocessor):
        self.html_dir = html_dir
        self.preprocessor = preprocessor
        self.results = []

    def extract_raw_topics(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        topic_container = soup.find("div", class_="detay-paylas")
        if not topic_container:
            return []
        links = topic_container.find_all("a", class_="btn btn-outline-secondary")
        return [link.get_text(strip=True) for link in links]

    def extract_publish_date(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        date_span = soup.find("span", class_="tarih")

        if date_span:
            # Match the first date in format dd.mm.yyyy
            match = re.search(r"\d{2}\.\d{2}\.\d{4}", date_span.get_text())
            if match:
                return match.group(0)

        return None  # or "unknown"

    def process_all_files(self):
        for filename in os.listdir(self.html_dir):
            if filename.endswith(".htm"):
                file_path = os.path.join(self.html_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    html = file.read()
                    raw_topics = self.extract_raw_topics(html)
                    dates = self.extract_publish_date(html)
                    # TODO add preprocessing
                    normalized_topics = raw_topics
                    self.results.append(
                        {
                            "filename": filename,
                            "topics": normalized_topics,
                            "dates": dates,
                        }
                    )
        return self

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.results)

    def save_to_csv(self, output_path: str):
        df = self.to_dataframe()
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
