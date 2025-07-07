import re
import unicodedata
import pandas as pd


class Preprocessor:
    def __init__(self, text_path: str):
        self.text_path = text_path
        self.data = None

    def load_data(self):
        # ! change if not kept as csv
        self.data = pd.read_csv(self.text_path)
        return self

    def normalize_category_text(self, text: str) -> str:
        if pd.isna(text):
            return "unknown"
        text = text.lower()
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        # ! may create a problem with turkish characters
        text = re.sub(r"[^a-z0-9]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def apply_normalization(self, column="category"):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        self.data["normalized_category"] = self.data[column].apply(
            self.normalize_category_text
        )
        return self

    def save_data(self, output_path: str):
        if self.data is not None:
            self.data.to_csv(output_path, index=False)
        else:
            raise ValueError("No data to save.")

    def get_data(self):
        return self.data
