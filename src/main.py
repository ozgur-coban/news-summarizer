from preprocessing import TurkishPreprocessor, TurkishNLTKPreprocessor
from scraping import TagExtractor, AA_NewsFetcher
from eda import Analyzer, Visualizer


def main():
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
    # tag_prep = TurkishPreprocessor("../data/raw/metadata/metadata.json")
    # tag_prep.load_data()
    # tag_prep.normalize_column("Title").normalize_column("Summary").normalize_column("Tags")
    # tag_prep.save("../data/processed/metadata_cleaned.jsonl")
    # prep = TurkishNLTKPreprocessor(
    #     path="../data/raw/metadata/metadata_copy.json", do_lema=True
    # )
    # prep.load_data()
    # # news-classification\src on  dev [!?] via 🐍 v3.12.7 took 7m59s
    # prep.normalize_column("Title").normalize_column("Summary").save(
    #     "../data/processed/metadata_cleaned_test_copy.jsonl"
    # )
    analyzer = Analyzer(
        source_file="../data/processed/metadata_cleaned_test_copy.jsonl"
    )
    # # analyzer.view_df()
    # # analyzer.info()
    # # analyzer.shape()
    # # analyzer.display_col("Tags_norm")
    # # tags_and_counts = analyzer.get_tag_counts()
    # analyzer.articles_per_day()  # Print per-day counts
    # analyzer.longest_shortest_day()  # Busiest and slowest day
    # analyzer.plot_trend()
    analyzer.most_common_words(field="Title_lemma")


if __name__ == "__main__":
    main()
