import pandas as pd


class Analyzer:
    def __init__(self, source_file):
        self.source_file = source_file
        self.df = None
        self.load_data()

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
