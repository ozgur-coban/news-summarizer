# english_preprocessor.py

import pandas as pd
import re
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# --- Download NLTK resources if not already present ---
# We need stopwords for filtering and wordnet for lemmatization.
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")
# ----------------------------------------------------

# --- Define English Stopwords ---
# Using the standard NLTK English stopwords list.
ENGLISH_STOPWORDS = set(stopwords.words("english"))
# You can add custom words here if needed, e.g., {"news", "say", "said"}
# CUSTOM_STOPWORDS = ENGLISH_STOPWORDS | {"news", "say", "said"}
# --------------------------------


class EnglishPreprocessor:
    def __init__(self, path=None):
        """path: input path to a JSONL file"""
        self.path = path
        self.data = None
        # Initialize the lemmatizer once for efficiency
        self.lemmatizer = WordNetLemmatizer()

    def load_data(self):
        """Loads data from the JSON/JSONL file specified in the path."""
        if self.path.endswith(".json") or self.path.endswith(".jsonl"):
            self.data = pd.read_json(self.path, lines=True)
        else:
            raise ValueError("Only JSON/JSONL is supported for this workflow.")
        return self

    def normalize_tags(self, tag_val):
        """
        Normalizes a string of comma-separated tags or a list of tags.
        - Converts to lowercase.
        - Removes extra whitespace.
        - Removes duplicate tags (preserves order).
        """
        if pd.isna(tag_val) or not tag_val:
            return []
        if isinstance(tag_val, list):
            tags = tag_val
        else:
            tags = [t.strip() for t in str(tag_val).split(",")]

        # Normalize and deduplicate, preserving order
        seen = set()
        norm_tags = []
        for tag in tags:
            tag_clean = tag.lower().strip()
            if tag_clean and tag_clean not in seen:
                norm_tags.append(tag_clean)
                seen.add(tag_clean)
        return norm_tags

    def normalize_text(self, text: str) -> str:
        """
        A comprehensive normalization pipeline for English text.
        1. Convert to lowercase.
        2. Remove accents and special characters.
        3. Remove non-alphanumeric characters (keeps letters and numbers).
        4. Lemmatize words to their root form.
        5. Remove stopwords.
        """
        if not isinstance(text, str) or pd.isna(text):
            return ""

        # 1. Convert to lowercase
        text = text.lower()

        # 2. Remove accents (e.g., café -> cafe)
        text = "".join(
            c
            for c in unicodedata.normalize("NFKD", text)
            if not unicodedata.combining(c)
        )

        # 3. Remove non-alphanumeric characters (keeping spaces)
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        # 4. Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()

        # 5. Lemmatize and remove stopwords
        tokens = []
        for word in text.split():
            # Lemmatize the word
            lemma = self.lemmatizer.lemmatize(word)
            # Add to list if it's not a stopword
            if lemma not in ENGLISH_STOPWORDS:
                tokens.append(lemma)

        return " ".join(tokens)

    def normalize_column(self, column: str, new_column: str = None):
        """
        Applies the full normalization pipeline to a specified dataframe column.
        Detects 'tags' column automatically for special handling.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Please call .load_data() first.")

        col_out = new_column or (column + "_norm")

        print(f"Normalizing column '{column}' into '{col_out}'...")
        if column.lower() == "tags":
            self.data[col_out] = self.data[column].apply(self.normalize_tags)
        else:
            self.data[col_out] = self.data[column].apply(self.normalize_text)
        return self

    def minimal_preprocess(self, text: str) -> str:
        """
        Minimal cleaning for Transformer models like BART:
        - Only fixes encoding and whitespace issues.
        - Keeps original casing, punctuation, and structure.
        """
        if not isinstance(text, str):
            text = str(text)

        text = text.replace("\xa0", " ")  # Non-breaking space
        text = text.replace("\u200b", "")  # Zero-width space
        text = re.sub(r"\s+", " ", text)  # Collapse multiple spaces/newlines/tabs
        text = text.strip()
        return text

    def minimal_preprocess_column(self, column: str, new_column: str = None):
        """Applies the minimal preprocessing pipeline to a specified column."""
        if self.data is None:
            raise ValueError("Data not loaded. Please call .load_data() first.")

        col_out = new_column or (column + "_minimal")

        print(
            f"Applying minimal preprocessing to column '{column}' into '{col_out}'..."
        )
        self.data[col_out] = self.data[column].apply(self.minimal_preprocess)
        return self

    def save(self, out_path: str):
        """Saves the processed dataframe to a new JSONL file."""
        if self.data is None:
            raise ValueError("No data to save.")

        print(f"Saving processed data to '{out_path}'...")
        self.data.to_json(out_path, orient="records", force_ascii=False, lines=True)
        print("✅ Save complete.")

    def get_data(self):
        """Returns the processed pandas DataFrame."""
        return self.data
