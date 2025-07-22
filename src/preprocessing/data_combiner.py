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
        joined_df = pd.merge(df_1, df_2, how="inner", on="Id")
        joined_df = joined_df.drop_duplicates(subset="Id", keep="first")
        return joined_df

    @staticmethod
    def join_df_union(df_1, df_2):
        combined_df = pd.concat([df_1, df_2], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset="Id", keep="first")
        return combined_df

    @staticmethod
    def get_df_info(df):
        print("head", df.head())
        print("info", df.info())
        print("shape", df.shape())
        print("columns", df.columns().tolist())
        print("random_rows", df.sample(5))

    @staticmethod
    def save(df: pd.DataFrame, path):
        df.to_json(path_or_buf=path, orient="records", force_ascii=False, lines=True)

    def run(self, path, join_type: str):
        if join_type == "inner":
            joined_df = DataCombiner.join_df_inner(self.metadata_df, self.body_df)
        elif join_type == "union":
            joined_df = DataCombiner.join_df_union(self.metadata_df, self.body_df)
        DataCombiner.save(df=joined_df, path=path)
