import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


class ResultAnalyzer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        # Convenience
        self.bertS_df = self.df[self.df["selection_type"] == "bertS"]
        self.rougeL_df = self.df[self.df["selection_type"] == "rougeL"]

    def percent_same_pick(self):
        pairs = self.df.groupby("article_id")["picked_summary"].apply(list)
        pairs = pairs.apply(lambda x: len(set(x)) == 1)
        percent = pairs.mean() * 100
        print(
            f"Percent of articles where bertS and rougeL pick the same summary: {percent:.2f}%"
        )
        return percent

    def average_scores(self):
        print("Average Scores (bertS pick):")
        print(self.bertS_df[["berts_f1", "rougeL", "rouge1", "bleu", "meteor"]].mean())
        print("\nAverage Scores (rougeL pick):")
        print(self.rougeL_df[["berts_f1", "rougeL", "rouge1", "bleu", "meteor"]].mean())

    def module_pick_counts(self):
        print("Picked module counts (bertS):")
        print(self.bertS_df["picked_module"].value_counts())
        print("\nPicked module counts (rougeL):")
        print(self.rougeL_df["picked_module"].value_counts())

    def plot_histograms(self, bins=40):
        plot_df = pd.concat(
            [
                self.bertS_df.assign(type="bertS pick"),
                self.rougeL_df.assign(type="rougeL pick"),
            ]
        )
        fig1 = px.histogram(
            plot_df,
            x="berts_f1",
            color="type",
            nbins=bins,
            barmode="overlay",
            opacity=0.6,
            title="BERTScore F1 Distribution",
            color_discrete_map={"bertS pick": "#1f77b4", "rougeL pick": "#ff7f0e"},
        )
        fig1.update_layout(
            xaxis_title="BERTScore F1",
            yaxis_title="Frequency",
            font=dict(size=18),
            title=dict(x=0.5, xanchor="center"),
            legend_title_text="Pick Type",
            bargap=0.1,
            plot_bgcolor="rgba(245,245,245,1)",
            paper_bgcolor="white",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        fig1.update_traces(marker_line_width=1, marker_line_color="black")
        fig1.show()

    def save_biggest_disagreements(
        self,
        n=10,
        bertscore_csv="biggest_bertscore_disagreements.csv",
        rougel_csv="biggest_rougel_disagreements.csv",
    ):
        # Merge bertS and rougeL picks by article_id
        merged = pd.merge(
            self.bertS_df.add_prefix("bertS_"),
            self.rougeL_df.add_prefix("rougeL_"),
            left_on="bertS_article_id",
            right_on="rougeL_article_id",
            suffixes=("_bertS", "_rougeL"),
        )

        # For BERTScore disagreement
        merged["bertscore_disagreement"] = (
            merged["bertS_berts_f1"] - merged["rougeL_berts_f1"]
        ).abs()
        biggest_bertscore = merged.sort_values(
            "bertscore_disagreement", ascending=False
        ).head(n)
        biggest_bertscore.to_csv(bertscore_csv, index=False, encoding="utf-8")

        # For ROUGE-L disagreement
        merged["rougel_disagreement"] = (
            merged["bertS_rougeL"] - merged["rougeL_rougeL"]
        ).abs()
        biggest_rougel = merged.sort_values(
            "rougel_disagreement", ascending=False
        ).head(n)
        biggest_rougel.to_csv(rougel_csv, index=False, encoding="utf-8")

        print(f"Saved top {n} BERTScore disagreement articles to {bertscore_csv}")
        print(f"Saved top {n} ROUGE-L disagreement articles to {rougel_csv}")

    def metrics_correlation(self):
        corr1 = self.bertS_df["berts_f1"].corr(self.bertS_df["rougeL"])
        corr2 = self.rougeL_df["berts_f1"].corr(self.rougeL_df["rougeL"])
        print(f"Correlation between BERTScore F1 and ROUGE-L (bertS pick): {corr1:.3f}")
        print(
            f"Correlation between BERTScore F1 and ROUGE-L (rougeL pick): {corr2:.3f}"
        )
        return corr1, corr2

    def summary_length_vs_score(self):
        self.bertS_df["summary_length"] = self.bertS_df["picked_summary"].apply(len)
        corr = self.bertS_df["summary_length"].corr(self.bertS_df["berts_f1"])
        print(
            f"Correlation between picked summary length and BERTScore F1 (bertS pick): {corr:.3f}"
        )

        fig = px.scatter(
            self.bertS_df,
            x="summary_length",
            y="berts_f1",
            title="Picked Summary Length vs BERTScore F1 (bertS pick)",
            labels={
                "summary_length": "Summary Length (chars)",
                "berts_f1": "BERTScore F1",
            },
            opacity=0.6,
            trendline="ols",
            template="plotly_white",
        )
        fig.update_layout(
            font=dict(size=18),
            title=dict(x=0.5, xanchor="center"),
            plot_bgcolor="rgba(245,245,245,1)",
            paper_bgcolor="white",
        )
        fig.update_traces(
            marker=dict(size=8, line=dict(width=1, color="DarkSlateGrey"))
        )
        fig.show()
        return corr
