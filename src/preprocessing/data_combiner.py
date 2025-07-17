import pandas as pd


class DataCombiner:
    def __init__(self, metadata_file, body_file):
        self.metadata_df = DataCombiner.load_data(metadata_file)
        self.body_df = DataCombiner.load_data(body_file)

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

    @staticmethod
    def join_df_inner(df_1, df_2):
        joined_df = pd.merge(df_1, df_2, how="inner")
        return joined_df

    @staticmethod
    def get_df_info(df):
        print("head", df.head())
        print("info", df.info())
        print("shape", df.shape())
        print("columns", df.columns().tolist())
        print("random_rows", df.sample(5))

    def run(self):
        return DataCombiner.join_df_inner(self.metadata_df, self.body_df)
