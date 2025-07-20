import pandas as pd


class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.data = df.copy()

    @staticmethod
    def load_data(file):
        """Load the JSONL metadata file into a DataFrame."""
        try:
            df = pd.read_json(file, lines=True)
            print(f"✅ Loaded {len(df)} records from {file}")
            return df
        except Exception as e:
            print(f"❌ Failed to load data: {e}")
            df = pd.DataFrame()  # Empty fallback
            return df

    def filter_columns(self, columns_to_keep=None):
        if columns_to_keep:
            self.data = self.data.filter(items=columns_to_keep)
        return self.data

    def report_missing(self):
        """Report missing value counts per column."""
        missing = self.data.isnull().sum()
        print("Missing values per column:\n", missing)
        return missing

    def drop_missing(self, columns=None):
        """Drop rows with missing values. If columns specified, only consider those columns."""
        if columns:
            self.data = self.data.dropna(subset=columns)
        else:
            self.data = self.data.dropna()
        return self.data

    def standardize_fields(self):
        """Standardize selected fields: datetimes, bools, strings, etc."""
        # Example standardizations; customize as needed!
        if "CreateDate" in self.data.columns:
            self.data["CreateDate"] = pd.to_datetime(
                self.data["CreateDate"], errors="coerce"
            )
        if "IsActive" in self.data.columns:
            self.data["IsActive"] = self.data["IsActive"].astype(bool)

        return self.data

    def save_df(self, save_path):
        if save_path:
            self.data.to_json(
                path_or_buf=f"{save_path}",
                orient="records",
                force_ascii=False,
                lines=True,
            )
        else:
            self.data.to_json(
                path_or_buf="data.jsonl",
                orient="records",
                force_ascii=False,
                lines=True,
            )
