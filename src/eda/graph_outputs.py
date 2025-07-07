import pandas as pd

import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, source_file):
        self.source_file = source_file
        self.df = pd.read_csv(self.source_file, encoding="utf-8-sig")

    def graph_counts_per_topics(self, selected_date="07.07.2025"):
        filtered = self.df[self.df["dates"] == selected_date].sort_values(
            by="count", ascending=True
        )

        plt.figure(figsize=(12, 6))
        plt.bar(filtered["topics"], filtered["count"])
        plt.xticks(rotation=45, ha="right")
        plt.title(f"Topic Frequencies on {selected_date}")
        plt.tight_layout()
        plt.show()
