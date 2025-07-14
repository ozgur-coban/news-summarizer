import pandas as pd
from preprocessing import TurkishNLTKPreprocessor
from scraping import TagExtractor, AA_NewsMetadataFetcher, AAArticleBodyFetcher
from eda import Analyzer, Visualizer, TextAnalyzer


def main():
    # fetcher = AA_NewsMetadataFetcher(
    #     start_page=1,
    #     max_pages=1000,
    #     category_id=2,
    #     keyword="***",
    #     save_to_file=True,
    #     save_file_path="../data/raw/metadata/metadata_gundem_13-7-2025.json",
    #     is_inplace=True,
    # )
    # fetcher.run()
    # for title, link in fetcher.results:
    #     print(f"- {title}\n  {link}")

    # prep = TurkishNLTKPreprocessor(
    #     path="../data/raw/metadata/metadata_copy.json", do_lema=True
    # )
    # prep.load_data()
    # # news-classification\src on  dev [!?] via 🐍 v3.12.7 took 7m59s
    # prep.normalize_column("Title").normalize_column("Summary").save(
    #     "../data/processed/metadata_cleaned_test_copy.jsonl"
    # )
    # analyzer = Analyzer(
    #     source_file="../data/processed/metadata_cleaned_test_copy.jsonl"
    # )
    # # analyzer.view_df()
    # # analyzer.info()
    # # analyzer.shape()
    # # analyzer.display_col("Tags_norm")
    # # tags_and_counts = analyzer.get_tag_counts()
    # analyzer.articles_per_day()  # Print per-day counts
    # analyzer.longest_shortest_day()  # Busiest and slowest day
    # analyzer.plot_trend()
    # analyzer.most_common_words(field="Title_lemma")
    # body_fetcher = AAArticleBodyFetcher(
    #     metadata_path="../data/raw/metadata/metadata_gundem_13-7-2025_copy.json",
    #     output_path="../data/raw/body/gundem_13-7-2025_body.jsonl",
    # )
    # body_fetcher.run(start=1, end=999)
    # prep = TurkishNLTKPreprocessor(
    #     path="../data/raw/body/full_articles/aa_full_articles_10000.jsonl",
    #     do_lema=False,
    # )
    # prep.load_data()
    # prep.normalize_column(column="full_text", new_column="prep_text").save(
    #     out_path="../data/processed/body/aa_prep_10000.jsonl"
    # )
    df = pd.read_json("../data/processed/body/aa_prep_10000.jsonl", lines=True)
    eda = TextAnalyzer(df)
    eda.length_stats()
    eda.length_hist()
    eda.most_common_words()


if __name__ == "__main__":
    main()
