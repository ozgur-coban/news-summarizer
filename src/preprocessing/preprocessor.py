# TODO change if not kept as csv
import re
import unicodedata
import pandas as pd


class Preprocessor:
    def __init__(self, text_path=None):
        self.text_path = text_path
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.text_path)
        return self

    def normalize_text(self, text: str) -> str:
        if pd.isna(text):
            return "unknown"

        # 1. Lowercase with Turkish support
        text = text.lower()

        # 2. Normalize to NFKD (decomposes letters like 'İ' into 'i' + dot)
        text = unicodedata.normalize("NFKD", text)

        # 3. Remove all combining marks (e.g., the dot above 'i')
        text = "".join([c for c in text if not unicodedata.combining(c)])

        # 4. Keep only Turkish letters, numbers, and spaces
        text = re.sub(r"[^a-z0-9çğıöşü\s]", " ", text)

        # 5. Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def normalize_topic_list(self, topic_list: list[str]) -> list[str]:
        return [self.normalize_text(t) for t in topic_list]

    def save_data(self, output_path: str):
        if self.data is not None:
            self.data.to_csv(output_path, index=False)
        else:
            raise ValueError("No data to save.")

    def get_data(self):
        return self.data
