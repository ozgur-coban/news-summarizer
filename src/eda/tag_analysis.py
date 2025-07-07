import pandas as pd
import ast


class TagAnalyzer:
    def __init__(self, source_file):
        self.source_file = source_file
        self.df = pd.read_csv(self.source_file)

    def get_unique_topics(self):
        unique_topics = set()

        for row in self.df["topics"]:
            if isinstance(row, str):
                try:
                    topics = ast.literal_eval(row)
                    if isinstance(topics, list):
                        unique_topics.update(topics)
                except (SyntaxError, ValueError):
                    continue  # skip malformed rows

        return sorted(unique_topics)

    def process_topic_counts_by_date(self, output_path: str):
        """
        Explodes topics while preserving 'date', counts frequency of each (date, topic) pair,
        and saves as a CSV.
        """
        # Convert stringified topic lists to real lists
        self.df["topics"] = self.df["topics"].apply(ast.literal_eval)

        # Explode topics while keeping date
        exploded = self.df.explode("topics").dropna(subset=["topics"])

        # Group and count (date, topic)
        topic_counts = (
            exploded.groupby(["dates", "topics"])
            .size()
            .reset_index(name="count")
            .sort_values(["dates", "count"], ascending=[True, False])
        )

        # Save the result
        topic_counts.to_csv(output_path, index=False, encoding="utf-8-sig")
