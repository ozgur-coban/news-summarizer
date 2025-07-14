import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


class TextAnalyzer:
    def __init__(self, df, text_col="prep_text", id_col="Id", title_col="Title"):
        self.df = df
        self.text_col = text_col
        self.id_col = id_col
        self.title_col = title_col

        # Add n_words column by counting words
        self.df["n_words"] = self.df[self.text_col].apply(lambda x: len(str(x).split()))

        # Filter out rows with fewer than 15 words
        self.df = self.cut_short_articles(self.df)

    def cut_short_articles(self, df, min_word_count=15):
        return df[df["n_words"] >= min_word_count]

    def length_stats(self):
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

    def length_hist(self, bins=30):
        plt.figure(figsize=(8, 4))
        self.df["n_words"].hist(bins=bins)
        plt.title("Distribution of Article Lengths (in words)")
        plt.xlabel("Number of Words")
        plt.ylabel("Number of Articles")
        plt.show()

    def most_common_words(self, n=30):
        words = []
        self.df[self.text_col].dropna().apply(lambda x: words.extend(str(x).split()))
        word_freq = Counter(words)
        print(f"Top {n} words:")
        for word, freq in word_freq.most_common(n):
            print(f"{word}: {freq}")
        # Optional: plot
        plt.figure(figsize=(10, 4))
        pd.Series(dict(word_freq.most_common(n))).plot(kind="bar")
        plt.title(f"Top {n} Most Common Words")
        plt.xlabel("Word")
        plt.ylabel("Frequency")
        plt.show()


# Usage Example:
# df = pd.read_json('your_cleaned_articles.jsonl', lines=True)
# eda = NewsTextEDA(df)
# eda.summary()
