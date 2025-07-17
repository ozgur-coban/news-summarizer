import pandas as pd


class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.data = df.copy()

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
        # Lowercase and strip whitespace for text fields
        for col in ["Title", "Summary", "full_text", "prep_title", "prep_text"]:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(str).str.lower().str.strip()
        # Remove leading/trailing spaces from all string/object columns
        obj_cols = self.data.select_dtypes(include="object").columns
        for col in obj_cols:
            self.data[col] = self.data[col].str.strip()
        return self.data
