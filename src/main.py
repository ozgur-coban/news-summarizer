from preprocessing import Preprocessor
from scraping import TagExtractor
from eda import TagAnalyzer, Visualizer


def main():
    pre = Preprocessor()
    extractor = TagExtractor(html_dir="../data/raw/html_articles", preprocessor=pre)

    extractor.process_all_files().save_to_csv("../data/processed/tags.csv")
    tag_analyzer = TagAnalyzer(source_file="../data/processed/tags.csv")
    tag_analyzer.process_topic_counts_by_date(
        output_path="../data/processed/tag_counts_by_date.csv"
    )
    visualizer = Visualizer(source_file="../data/processed/tag_counts_by_date.csv")
    visualizer.graph_counts_per_topics()


if __name__ == "__main__":
    main()
