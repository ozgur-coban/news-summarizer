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

    def process_topic_counts(self, output_path: str):
        """
        Converts stringified topic lists to actual lists, explodes, counts, and saves frequency.
        """
        # Convert strings to real lists
        self.df["topics"] = self.df["topics"].apply(ast.literal_eval)

        # Explode and count
        topic_counts = self.df["topics"].explode().dropna().value_counts().reset_index()
        topic_counts.columns = ["topic", "count"]

        # Save to CSV
        topic_counts.to_csv(output_path, index=False, encoding="utf-8-sig")
