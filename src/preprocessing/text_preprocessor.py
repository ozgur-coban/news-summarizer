import pandas as pd
import re
import unicodedata
import nltk
import stanza

# Download Turkish stopwords if not already present
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

TURKISH_STOPWORDS = set(nltk.corpus.stopwords.words("turkish"))
# TODO
# ADDITIONAL_STOPWORDS = {"nin", "ın", "nın", "in"}
# CUSTOM_STOPWORDS = TURKISH_STOPWORDS | ADDITIONAL_STOPWORDS


class TurkishNLTKPreprocessor:
    def __init__(self, path=None, do_lema=False):
        self.path = path
        self.data = None
        self.do_lema = do_lema
        self.nlp = None

    def load_data(self):
        if self.path.endswith(".json") or self.path.endswith(".jsonl"):
            self.data = pd.read_json(self.path, lines=True)
        else:
            raise ValueError("Only JSON/JSONL supported for this news workflow.")
        return self

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

    def normalize_text(self, text: str) -> str:
        if not isinstance(text, str) or pd.isna(text):
            return ""
        text = text.replace("\xa0", " ")
        text = self.turkish_lower(text)
        text = unicodedata.normalize("NFKD", text)
        text = "".join([c for c in text if not unicodedata.combining(c)])
        text = re.sub(r"[^a-z0-9çğıöşü\s]", " ", text)
        text = re.sub(r"\bamp\b", " ", text)  # <-- Remove standalone 'amp'
        text = re.sub(r"\s+", " ", text).strip()
        tokens = [t for t in text.split() if t not in TURKISH_STOPWORDS]
        return " ".join(tokens)

    def lemmatize_text(self, text: str) -> str:
        # Run normalization first
        text = self.normalize_text(text)
        if not text:
            return ""
        if self.nlp is None:
            try:
                stanza.download("tr")
            except Exception:
                pass
            self.nlp = stanza.Pipeline(
                lang="tr", processors="tokenize,mwt,pos,lemma", verbose=False
            )
        doc = self.nlp(text)
        return " ".join(
            [
                word.lemma
                for sent in doc.sentences
                for word in sent.words
                if word.lemma and word.lemma not in TURKISH_STOPWORDS
            ]
        )

    def normalize_tags(self, tag_val):
        if pd.isna(tag_val) or not tag_val:
            return []
        if isinstance(tag_val, list):
            tags = tag_val
        else:
            tags = str(tag_val).split(",")
        return [self.normalize_text(tag) for tag in tags if tag]

    def normalize_column(self, column, new_column=None):
        if self.data is None:
            raise ValueError("Data not loaded")
        col = new_column or (column + ("_lemma" if self.do_lema else "_norm"))
        if column.lower() == "tags":
            self.data[col] = self.data[column].apply(self.normalize_tags)
        else:
            if self.do_lema:
                self.data[col] = self.data[column].apply(self.lemmatize_text)
            else:
                self.data[col] = self.data[column].apply(self.normalize_text)
        return self

    def save(self, out_path):
        self.data.to_json(out_path, orient="records", force_ascii=False, lines=True)

    def get_data(self):
        return self.data


# Usage Example:
# pre = TurkishNLTKPreprocessor("yourfile.jsonl", do_lema=True).load_data()
# pre.normalize_column("Title").normalize_column("Summary").save("output.jsonl")
