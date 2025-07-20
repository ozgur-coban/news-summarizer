import pandas as pd
import re


class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.data = df.copy()

    @staticmethod
    def load_data(file):
        try:
            df = pd.read_json(file, lines=True)
            print(f"✅ Loaded {len(df)} records from {file}")
            return df
        except Exception as e:
            print(f"❌ Failed to load data: {e}")
            return pd.DataFrame()

    def filter_columns(self, columns_to_keep=None):
        if columns_to_keep:
            self.data = self.data.filter(items=columns_to_keep)
        return self.data

    def report_missing(self):
        missing = self.data.isnull().sum()
        print("Missing values per column:\n", missing)
        return missing

    def drop_missing(self, columns=None):
        if columns:
            self.data = self.data.dropna(subset=columns)
        else:
            self.data = self.data.dropna()
        return self.data

    def standardize_fields(self):
        if "CreateDate" in self.data.columns:
            self.data["CreateDate"] = pd.to_datetime(
                self.data["CreateDate"], errors="coerce"
            )
        if "IsActive" in self.data.columns:
            self.data["IsActive"] = self.data["IsActive"].astype(bool)
        return self.data

    @staticmethod
    def clean_aa_english_article(text):
        if not isinstance(text, str):
            return text
        text = text.lstrip()
        match = re.match(
            r"^(([A-Z][A-Z\s\-]+, [A-Za-z]+)|([A-Z][A-Z\s\-]+)|([A-Z], [A-Za-z]+)|(, [A-Za-z]+))\s*",
            text,
        )
        if match:
            text = text[match.end() :].lstrip()

        footer_patterns = [
            r"Anadolu Agency website contains only.*",
            r"Please contact us for subscription options.*",
            r"Related topics.*",
            r"Bu haberi paylaşın.*",
        ]
        for pat in footer_patterns:
            text = re.sub(pat, "", text, flags=re.DOTALL)
        text = text.strip()
        return text

    def clean_english_articles(self):
        if "Title" in self.data.columns:
            before = len(self.data)
            self.data = self.data[
                ~self.data["Title"].str.contains("Morning Briefing", na=False)
            ]
            after = len(self.data)
            print(f"Removed {before - after} 'Morning Briefing' articles.")
        if "full_text" in self.data.columns:
            self.data["full_text"] = self.data["full_text"].apply(
                self.clean_aa_english_article
            )
        return self.data

    def remove_duplicates(self):
        before = len(self.data)
        self.data = self.data.drop_duplicates(subset="Id", keep="first")
        after = len(self.data)
        print(f"Removed {before - after} duplicate articles by Id.")
        return self.data

    def save_df(self, save_path):
        self.data.to_json(
            path_or_buf=save_path,
            orient="records",
            force_ascii=False,
            lines=True,
        )


# Usage Example:
# df = DataCleaner.load_data("input.jsonl")
# cleaner = DataCleaner(df)
# cleaner.clean_english_articles()
# cleaner.remove_duplicates()
# cleaner.save_df("output.jsonl")
