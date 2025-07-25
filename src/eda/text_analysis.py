import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px


class TextAnalyzer:
    def __init__(self, source_file, id_col="Id", title_col="Title"):
        self.source_file = source_file
        self.df = None
        self._load_data()

        self.id_col = id_col
        self.title_col = title_col

    def _load_data(self):
        """Load the JSONL metadata file into a DataFrame."""
        try:
            self.df = pd.read_json(self.source_file, lines=True)
            print(f"✅ Loaded {len(self.df)} records from {self.source_file}")
        except Exception as e:
            print(f"❌ Failed to load data: {e}")
            self.df = pd.DataFrame()  # Empty fallback

    @staticmethod
    def _calculate_word_count(df, text_col, new_col="n_words"):
        """
        Adds/updates a word count column for the specified text column.

        Args:
            df (pd.DataFrame): The DataFrame.
            text_col (str): The name of the text column.
            new_col (str): The name for the word count column (default: 'n_words').
        Returns:
            pd.DataFrame: The DataFrame with the new column.
        """
        df[new_col] = df[text_col].apply(
            lambda x: len(str(x).split()) if pd.notnull(x) else 0
        )
        return df

    def length_stats(self, text_col):
        TextAnalyzer._calculate_word_count(df=self.df, text_col=text_col)
        print("Article Count:", len(self.df))
        print("Min length (words):", self.df["n_words"].min())
        print("Max length (words):", self.df["n_words"].max())
        print("Mean length (words):", self.df["n_words"].mean())
        print("Median length (words):", self.df["n_words"].median())
        print("10 shortest articles:")
        print(
            self.df[[self.id_col, self.title_col, "n_words"]]
            .sort_values("n_words")
            .head(10)
        )
        print("10 longest articles:")
        print(
            self.df[[self.id_col, self.title_col, "n_words"]]
            .sort_values("n_words", ascending=False)
            .head(10)
        )

    def length_hist(self, text_col, bins=30):
        TextAnalyzer._calculate_word_count(df=self.df, text_col=text_col)
        fig = px.histogram(
            self.df,
            x="n_words",
            nbins=bins,
            title="Distribution of Article Lengths (in words)",
            labels={"n_words": "Number of Words"},
            opacity=0.85,
            color_discrete_sequence=["#1976D2"],
        )
        fig.update_layout(
            xaxis_title="Number of Words", yaxis_title="Number of Articles", bargap=0.07
        )
        fig.show()

    def most_common_words(self, text_col, n=30, ngram=1):
        ngram_list = []
        for text in self.df[text_col].dropna():
            tokens = str(text).split()
            if len(tokens) < ngram:
                continue
            ngrams = zip(*[tokens[i:] for i in range(ngram)])
            ngram_list.extend([" ".join(ng) for ng in ngrams])
        ngram_freq = Counter(ngram_list)
        print(f"Top {n} {ngram}-grams:")
        for ngram_str, freq in ngram_freq.most_common(n):
            print(f"{ngram_str}: {freq}")

        # Plotly barplot
        top_ngrams = ngram_freq.most_common(n)
        df_plot = pd.DataFrame(top_ngrams, columns=["Ngram", "Frequency"])
        fig = px.bar(
            df_plot,
            x="Ngram",
            y="Frequency",
            title=f"Top {n} Most Common {ngram}-grams",
            labels={"Ngram": f"{ngram}-gram", "Frequency": "Frequency"},
            color="Frequency",
            color_continuous_scale="Teal",
        )
        fig.update_layout(
            xaxis_title=f"{ngram}-gram", yaxis_title="Frequency", xaxis_tickangle=-45
        )
        fig.show()


# Usage Example:
# df = pd.read_json('your_cleaned_articles.jsonl', lines=True)
# eda = NewsTextEDA(df)
# eda.summary()
