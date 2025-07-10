import pandas as pd
import re
import unicodedata


class TurkishPreprocessor:
    def __init__(self, path=None):
        self.path = path
        self.data = None

    def load_data(self):
        if self.path.endswith(".json") or self.path.endswith(".jsonl"):
            self.data = pd.read_json(self.path, lines=True)
        else:
            raise ValueError("Only JSON/JSONL supported for this news workflow.")
        return self

    @staticmethod
    def normalize_text(text: str) -> str:
        if not isinstance(text, str) or pd.isna(text):
            return ""
        # Turkish lowercasing (basic: works for most practical uses)
        text = text.replace("I", "ı").replace("İ", "i").lower()
        # Unicode normalization
        text = unicodedata.normalize("NFKD", text)
        # Remove combining marks
        text = "".join([c for c in text if not unicodedata.combining(c)])
        # Remove non-Turkish letters, numbers, space
        text = re.sub(r"[^a-z0-9çğıöşü\s]", " ", text)
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def normalize_tags(tag_val):
        if pd.isna(tag_val) or not tag_val:
            return []
        if isinstance(tag_val, list):
            tags = tag_val
        else:
            tags = str(tag_val).split(",")
        return [TurkishPreprocessor.normalize_text(tag) for tag in tags if tag]

    def normalize_column(self, column, new_column=None):
        if self.data is None:
            raise ValueError("Data not loaded")
        col = new_column or (column + "_norm")
        if column.lower() == "tags":
            self.data[col] = self.data[column].apply(self.normalize_tags)
        else:
            self.data[col] = self.data[column].apply(self.normalize_text)
        return self

    def save(self, out_path):
        self.data.to_json(out_path, orient="records", force_ascii=False, lines=True)

    def get_data(self):
        return self.data
