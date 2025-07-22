import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


class Analyzer:
    def __init__(self, source_file):
        self.source_file = source_file
        self.df = None
        self._load_data()
        self.tags = set()
        self.df["date"] = pd.to_datetime(
            self.df["CreateDateString"], format="%d.%m.%Y", errors="coerce"
        )

    # DF Analysis
    def _load_data(self):
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
    def get_tag_counts(self, col="Tags"):
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

    def plot_tag_counts(self, col="Tags", top_n=20):
        tag_counter = self.get_tag_counts(col)
        if not tag_counter:
            print("No tags found.")
            return
        common_tags = tag_counter.most_common(top_n)
        tags, counts = zip(*common_tags)
        plt.figure(figsize=(10, 4))
        plt.bar(tags, counts)
        plt.title(f"Top {top_n} Tags")
        plt.xlabel("Tag")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    # Date Analysis
    def articles_per_day(self, print_bool=False):
        counts = self.df["date"].value_counts().sort_index()
        # print(counts)
        if print_bool:
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
        busiest_single = busiest.index[0]
        slowest_single = slowest.index[0]
        print(f"Most articles: {max_count} on {busiest_single}")
        print(f"Fewest articles: {min_count} on {slowest_single}")
        return busiest, slowest

    def articles_per_month_around_date(
        self, selected_date, months_window=3, date_col="date"
    ):
        """
        Plots monthly article counts centered around selected_date ± months_window.

        Args:
            selected_date (str or pd.Timestamp): Central date (e.g., "2024-04-01")
            months_window (int): Number of months before and after to include.
            date_col (str): Name of date column in DataFrame.
        """
        # Parse date
        if not isinstance(selected_date, pd.Timestamp):
            selected_date = pd.to_datetime(selected_date)
        # Filter window
        start = selected_date - pd.DateOffset(months=months_window)
        end = selected_date + pd.DateOffset(months=months_window)
        mask = (self.df[date_col] >= start) & (self.df[date_col] <= end)
        df_window = self.df[mask]
        # Group by month
        monthly = df_window.groupby(df_window[date_col].dt.to_period("M"))["Id"].count()
        # Plot
        plt.figure(figsize=(10, 4))
        monthly.plot(kind="bar")
        plt.title(f"Articles per Month Around {selected_date.strftime('%Y-%m-%d')}")
        plt.xlabel("Month")
        plt.ylabel("Article Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        return monthly

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

    def plot_tag_coverage_over_time(
        self, tag, date_col="date", tags_col="Tags", top_n_months=None
    ):
        """
        Plots the number of articles per month containing the specified tag.
        """
        # Always lower for robust matching
        tag_lower = tag.lower()
        mask = self.df[tags_col].apply(
            lambda tags: tag_lower in [str(t).lower() for t in tags]
            if isinstance(tags, list)
            else tag_lower in str(tags).lower()
        )
        tag_df = self.df[mask]
        if tag_df.empty:
            print(f'No articles found with tag "{tag}"')
            return
        monthly_counts = tag_df.groupby(tag_df[date_col].dt.to_period("M"))[
            "Id"
        ].count()
        if top_n_months:
            monthly_counts = (
                monthly_counts.sort_values(ascending=False)
                .head(top_n_months)
                .sort_index()
            )
        plt.figure(figsize=(10, 4))
        monthly_counts.plot(kind="bar")
        plt.title(f'Coverage of "{tag}" Over Time')
        plt.xlabel("Month")
        plt.ylabel("Number of Articles")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
        return monthly_counts
