# TODO make sure that all of them are under detay-paylas exactly
import os
import pandas as pd
from bs4 import BeautifulSoup

from preprocessing.preprocessor import Preprocessor


class TopicExtractor:
    def __init__(self, html_dir: str, preprocessor: Preprocessor):
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

    def process_all_files(self):
        for filename in os.listdir(self.html_dir):
            if filename.endswith(".htm"):
                file_path = os.path.join(self.html_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    html = file.read()
                    raw_topics = self.extract_raw_topics(html)
                    normalized_topics = self.preprocessor.normalize_topic_list(
                        raw_topics
                    )
                    self.results.append(
                        {"filename": filename, "topics": normalized_topics}
                    )
        return self

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.results)

    def save_to_csv(self, output_path: str):
        df = self.to_dataframe()
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
