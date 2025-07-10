import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter


class Analyzer:
    def __init__(self, source_file):
        self.source_file = source_file
        self.df = None
        self.load_data()
        self.tags = set()
        self.df["date"] = pd.to_datetime(
            self.df["CreateDateString"], format="%d.%m.%Y", errors="coerce"
        )

    # DF Analysis
    def load_data(self):
        """Load the JSONL metadata file into a DataFrame."""
        try:
            self.df = pd.read_json(self.source_file, lines=True)
            print(f"✅ Loaded {len(self.df)} records from {self.source_file}")
        except Exception as e:
            print(f"❌ Failed to load data: {e}")
            self.df = pd.DataFrame()  # Empty fallback

    def view_df(self, n=5):
        """Print the first n rows of the DataFrame."""
        print(self.df.head(n))

    def info(self):
        """Print summary info (columns, types, non-nulls, etc)."""
        print(self.df.info())

    def shape(self):
        """Return DataFrame shape (rows, columns)."""
        print(self.df.shape)

    def show_columns(self):
        """Print the columns in the DataFrame."""
        print(self.df.columns.tolist())

    def preview_random(self, n=5):
        """Show a random sample of rows."""
        print(self.df.sample(n))

    def describe_dates(self, date_col="CreateDateString"):
        """Print the min/max date (if available)."""
        if date_col in self.df.columns:
            print("Earliest date:", self.df[date_col].min())
            print("Latest date:", self.df[date_col].max())
        else:
            print(f"No '{date_col}' column found.")

    def missing_report(self):
        """Show count of missing values per column."""
        print(self.df.isnull().sum())

    def display_col(self, col):
        for value in self.df[col]:
            print(value)

    # Tag Analysis
    def get_tag_counts(self, col="Tags_norm"):
        tag_counter = Counter()
        for tag_list in self.df[col]:
            if isinstance(tag_list, list):
                for tag in tag_list:
                    if tag:  # skip empty
                        tag_counter.update([tag])
            elif isinstance(tag_list, str):
                # Assume tags in string are comma-separated, or just one tag
                tags = [
                    tag.strip().lower() for tag in tag_list.split(",") if tag.strip()
                ]
                tag_counter.update(tags)
            # Else: skip (could be None, float, etc.)
        return tag_counter

    # Date Analysis
    def articles_per_day(self):
        counts = self.df["date"].value_counts().sort_index()
        print(counts)
        return counts

    def articles_per_week(self):
        # Group by year-week
        weekly = self.df.groupby(self.df["date"].dt.isocalendar().week)["Id"].count()
        print(weekly)
        return weekly

    def articles_per_month(self):
        monthly = self.df.groupby(self.df["date"].dt.to_period("M"))["Id"].count()
        print(monthly)
        return monthly

    def longest_shortest_day(self):
        counts = self.articles_per_day()
        max_count = counts.max()
        min_count = counts.min()
        busiest = counts[counts == max_count]
        slowest = counts[counts == min_count]
        print(f"Most articles: {max_count} on {list(busiest.index)}")
        print(f"Fewest articles: {min_count} on {list(slowest.index)}")
        return busiest, slowest

    def plot_trend(self, freq="D"):
        # freq: "D"=daily, "W"=weekly, "M"=monthly
        if freq == "D":
            counts = self.articles_per_day()
        elif freq == "W":
            counts = self.articles_per_week()
        else:
            counts = self.articles_per_month()
        counts.plot(kind="line", marker="o")
        plt.title(f"Article frequency {freq}")
        plt.ylabel("Article Count")
        plt.xlabel("Date")
        plt.tight_layout()
        plt.show()


# Title and Summary Analysis
# def most_common_words(self, field="Title_norm", n=20):
#     word_counter = Counter()
#     for text in self.df[field].dropna():
#         words = re.findall(
#             r"\b[\wçğıöşü]+\b", text.lower()
#         )  # Handles Turkish chars
#         word_counter.update(words)
#     print(f"Most common words in {field}:")
#     for word, count in word_counter.most_common(n):
#         print(f"{word}: {count}")
