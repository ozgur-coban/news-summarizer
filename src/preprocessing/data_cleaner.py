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
    def sub_clean_aa_english_article(text):
        if not isinstance(text, str):
            return text

        # --- Start of Corrected Section ---

        # This revised regex correctly handles unicode characters like 'ü'.
        #
        # How it works:
        # ^(?:\"full_text\":\")?  - Optionally matches the 'full_text' wrapper.
        # ([A-Z\s/]{3,})          - Matches a prefix of at least 3 uppercase letters, spaces, or slashes.
        #                         (This prevents it from matching acronyms like "US").
        # (?=[A-Z][^A-Z\s])      - This is the crucial lookahead. It ensures the prefix is followed by
        #                         a capitalized word. It checks for:
        #                         [A-Z]: An uppercase letter (like 'T' in 'Türkiye').
        #                         [^A-Z\s]: A character that is NOT an uppercase letter or a space.
        #                                  This correctly matches 'ü', 'u', etc.
        #
        prefix_pattern = r"^(?:\"full_text\":\")?([A-Z\s/]{3,})(?=[A-Z][^A-Z\s])"

        text = re.sub(prefix_pattern, "", text).strip()

        # --- End of Corrected Section ---

        if text.endswith('"'):
            text = text[:-1]

        # Remove footers
        footer_patterns = [
            r"Anadolu Agency website contains only.*",
            r"Please contact us for subscription options.*",
            r"Related topics.*",
            r"Bu haberi paylaşın.*",
        ]
        for pat in footer_patterns:
            text = re.sub(pat, "", text, flags=re.DOTALL)

        return text.strip()

    def clean_english_articles(self):
        if "Title" in self.data.columns:
            before = len(self.data)
            self.data = self.data[
                ~self.data["Title"].str.contains("Morning Briefing", na=False)
            ]
            after = len(self.data)
            print(f"Removed {before - after} 'Morning Briefing' articles.")
        if "full_text" in self.data.columns:
            # The .apply call now uses the corrected function
            self.data["full_text"] = self.data["full_text"].apply(
                self.sub_clean_aa_english_article
            )
        return self.data

    def remove_duplicates(self):
        before = len(self.data)
        self.data = self.data.drop_duplicates(subset="Id", keep="first")
        after = len(self.data)
        print(f"Removed {before - after} duplicate articles by Id.")
        return self.data

    def filter_short_texts(self, min_length=150):
        if "full_text_minimal" in self.data.columns:
            before = len(self.data)
            self.data = self.data[
                self.data["full_text_minimal"].apply(lambda x: len(x) >= min_length)
            ]
            after = len(self.data)
            print(
                f"Filtered out {before - after} articles with 'full_text_minimal' shorter than {min_length} characters."
            )
        return self.data

    def save_df(self, save_path):
        self.data.to_json(
            path_or_buf=save_path,
            orient="records",
            force_ascii=False,
            lines=True,
        )
