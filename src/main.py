from preprocessing import TurkishPreprocessor
from scraping import TagExtractor, AA_NewsFetcher
from eda import TagAnalyzer, Visualizer


def main():
    # pre = TurkishPreprocessor()
    # extractor = TagExtractor(html_dir="../data/raw/html_articles", TurkishPreprocessor=pre)

    # extractor.process_all_files().save_to_csv("../data/processed/tags.csv")
    # tag_analyzer = TagAnalyzer(source_file="../data/processed/tags.csv")
    # tag_analyzer.process_topic_counts_by_date(
    #     output_path="../data/processed/tag_counts_by_date.csv"
    # )
    # visualizer = Visualizer(source_file="../data/processed/tag_counts_by_date.csv")
    # visualizer.graph_counts_per_topics()

    # fetcher = AA_NewsFetcher(
    #     start_page=101,
    #     max_pages=49,
    #     category_id=2,
    #     keyword="***",
    #     save_to_file=True,
    #     save_file_path="../data/raw/metadata/metadata.json",
    #     is_inplace=False,
    # )
    # fetcher.run()
    # for title, link in fetcher.results:
    #     print(f"- {title}\n  {link}")
    prep = TurkishPreprocessor("../data/raw/metadata/metadata.json")
    prep.load_data()
    prep.normalize_column("Title").normalize_column("Summary").normalize_column("Tags")
    prep.save("../data/processed/metadata_cleaned.jsonl")


if __name__ == "__main__":
    main()
