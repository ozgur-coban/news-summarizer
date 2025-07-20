import pandas as pd
import re
import unicodedata
import nltk

# Download Turkish stopwords if not already present
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

TURKISH_STOPWORDS = set(nltk.corpus.stopwords.words("turkish"))
# TODO
# ADDITIONAL_STOPWORDS = {"nin", "ın", "nın", "in"}
# CUSTOM_STOPWORDS = TURKISH_STOPWORDS | ADDITIONAL_STOPWORDS


class TurkishPreprocessor:
    def __init__(
        self,
        path=None,
    ):
        """path: input path"""
        self.path = path
        self.data = None

        self.nlp = None

    def load_data(self):
        if self.path.endswith(".json") or self.path.endswith(".jsonl"):
            self.data = pd.read_json(self.path, lines=True)
        else:
            raise ValueError("Only JSON/JSONL supported for this news workflow.")
        return self

    def remove_turkish_suffix(text):
        # Possessive (nin/nın/nun/nün), Locative (da/de/ta/te)
        pattern = r"\b([a-zçğıöşü]+)[‘’'`´]?(nin|nın|nun|nün|da|de|ta|te)\b"
        # Replace with just the base word (group 1)
        return re.sub(pattern, r"\1", text, flags=re.IGNORECASE)

    @staticmethod
    def turkish_lower(text):
        if not isinstance(text, str):
            return ""
        return (
            text.replace("I", "ı")
            .replace("İ", "i")
            .replace("Ş", "ş")
            .replace("Ğ", "ğ")
            .replace("Ü", "ü")
            .replace("Ö", "ö")
            .replace("Ç", "ç")
            .lower()
        )

    def normalize_tags(self, tag_val):
        """
        Normalize tags without removing ',' or mangling tag structure.
        Supports both comma-separated strings and list input.
        """
        # Handle missing/empty input
        if pd.isna(tag_val) or not tag_val:
            return []
        # If already a list, normalize each tag
        if isinstance(tag_val, list):
            tags = tag_val
        else:
            # If string, split on comma but preserve commas within tags by not stripping aggressively
            tags = [t.strip() for t in str(tag_val).split(",")]

        # Normalize each tag: lowercase, strip accents, strip extra whitespace
        def norm_tag(tag):
            tag = self.turkish_lower(tag)
            tag = unicodedata.normalize("NFKD", tag)
            tag = "".join([c for c in tag if not unicodedata.combining(c)])
            # Optionally, strip ONLY leading/trailing punctuation (but NOT inside the tag)
            tag = tag.strip()
            return tag

        return [norm_tag(tag) for tag in tags if tag]

    def normalize_text(self, text: str) -> str:
        if not isinstance(text, str) or pd.isna(text):
            return ""
        text = text.replace("\xa0", " ")
        text = self.turkish_lower(text)
        text = TurkishPreprocessor.remove_turkish_suffix(text)
        text = unicodedata.normalize("NFKD", text)
        text = "".join([c for c in text if not unicodedata.combining(c)])
        text = re.sub(r"[^a-z0-9çğıöşü\s]", " ", text)
        text = re.sub(r"\bamp\b", " ", text)  # <-- Remove standalone 'amp'
        text = re.sub(r"\s+", " ", text).strip()
        tokens = [t for t in text.split() if t not in TURKISH_STOPWORDS]
        return " ".join(tokens)

    # def lemmatize_text(self, text: str) -> str:
    #     # Run normalization first
    #     text = self.normalize_text(text)
    #     if not text:
    #         return ""
    #     if self.nlp is None:
    #         try:
    #             stanza.download("tr")
    #         except Exception:
    #             pass
    #         self.nlp = stanza.Pipeline(
    #             lang="tr", processors="tokenize,mwt,pos,lemma", verbose=False
    #         )
    #     doc = self.nlp(text)
    #     return " ".join(
    #         [
    #             word.lemma
    #             for sent in doc.sentences
    #             for word in sent.words
    #             if word.lemma and word.lemma not in TURKISH_STOPWORDS
    #         ]
    #     )

    def normalize_column(self, column, new_column=None):
        if self.data is None:
            raise ValueError("Data not loaded")
        col = new_column or (column + "_norm")

        # Auto-detect if this is a tags column (case-insensitive for robustness)
        if column.lower() == "tags":
            self.data[col] = self.data[column].apply(self.normalize_tags)
        else:
            self.data[col] = self.data[column].apply(self.normalize_text)
        return self

    def minimal_preprocess(self, text):
        """
        Minimal cleaning for TURNA LLM:
        - Keeps original text and structure
        - Fixes encoding and whitespace issues only
        """
        if not isinstance(text, str):
            text = str(text)
        text = text.replace("\xa0", " ")  # Non-breaking space
        text = text.replace("\u200b", "")  # Zero-width space
        text = re.sub(r"\s+", " ", text)  # Collapse multiple spaces/newlines/tabs
        text = text.strip()
        return text

    def minimal_preprocess_column(self, column, new_column=None):
        if self.data is None:
            raise ValueError("Data not loaded")
        col = new_column or (column + "_minimal")
        self.data[col] = self.data[column].apply(self.minimal_preprocess)
        return self

    def save(self, out_path):
        self.data.to_json(out_path, orient="records", force_ascii=False, lines=True)

    def get_data(self):
        return self.data


# Usage Example:
# pre = TurkishNLTKPreprocessor("yourfile.jsonl", do_lema=True).load_data()
# pre.normalize_column("Title").normalize_column("Summary").save("output.jsonl")
