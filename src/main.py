import pandas as pd
from preprocessing import (
    TurkishNLTKPreprocessor,
    DataCleaner,
    DataCombiner,
    EnglishNLTKPreprocessor,
)
from scraping import (
    AA_NewsMetadataFetcher,
    AAArticleBodyFetcher,
    AA_EnglishNewsMetadataFetcher,
    AA_EnglishArticleBodyFetcher,
)
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
    # fetcher = AA_EnglishNewsMetadataFetcher(
    #     start_page=1,
    #     max_pages=500,  # 3 x 100 = 300 news
    #     category_id=4,  # "World" (choose as you want)
    #     keyword="* * *",  # for all news
    #     save_to_file=True,
    #     save_file_path="english_news_metadata.jsonl",
    #     is_inplace=True,
    #     page_size=20,  # up to 100
    # )
    # fetcher.run()

    # for title, link in fetcher.results:
    #     print(f"- {title}\n  {link}")

    # body_fetcher = AAArticleBodyFetcher(
    #     metadata_path="../data/raw/metadata/metadata_gundem_13-7-2025_copy.json",
    #     output_path="../data/raw/body/gundem_13-7-2025_body.jsonl",
    # )
    # body_fetcher.run(start=1, end=999)

    # body_fetcher = AA_EnglishArticleBodyFetcher(
    #     metadata_path="../data/raw/metadata/english_news_metadata_17-7-2025.jsonl",
    #     output_path="../data/raw/body/full_articles/aa_eng_full_articles_10000.jsonl",
    # )
    # body_fetcher.run(start=1, end=9999)

    # metadata = "../data/raw/metadata/english_news_metadata_17-7-2025.jsonl"
    # body = "../src/tests/output_no_duplicates.jsonl"
    # metadata_df = DataCleaner.load_data(metadata)
    # body_df = DataCleaner.load_data(body)
    # metadata_cleaner = DataCleaner(metadata_df)
    # body_cleaner = DataCleaner(body_df)
    # metadata_cleaner.filter_columns(
    #     columns_to_keep=[
    #         "Id",
    #         "Summary",
    #     ]
    # )
    # metadata_cleaner.drop_missing()
    # metadata_cleaner.standardize_fields()
    # metadata_cleaner.save_df(save_path="./eng_metadata.jsonl")
    # body_cleaner.filter_columns(columns_to_keep=["Id", "full_text"])
    # body_cleaner.drop_missing()
    # body_cleaner.standardize_fields()
    # body_cleaner.save_df(save_path="./eng_body.jsonl")
    # prep = TurkishNLTKPreprocessor(path="./metadata.jsonl")
    # prep.load_data()
    # prep.minimal_preprocess_column(column="Summary")
    # prep.save(out_path="../data/feed/clean_metadata.jsonl")
    # prep = TurkishNLTKPreprocessor(path="./body.jsonl")
    # prep.load_data()
    # prep.minimal_preprocess_column("full_text")
    # prep.save(out_path="../data/feed/clean_body.jsonl")
    # !
    # prep = EnglishNLTKPreprocessor(path="../data/raw/filtered/eng_metadata.jsonl")
    # prep.load_data()
    # prep.minimal_preprocess_column("Summary")
    # prep.save(out_path="../data/feed/clean_metadata_eng.jsonl")
    # prep = EnglishNLTKPreprocessor(path="../data/raw/filtered/eng_body.jsonl")
    # prep.load_data()
    # prep.minimal_preprocess_column("full_text")
    # prep.save(out_path="../data/feed/clean_body_eng.jsonl")
    # !
    combiner = DataCombiner(
        metadata_file="../data/feed/clean_metadata_eng.jsonl",
        body_file="../data/feed/clean_body_eng.jsonl",
    )
    combiner.run(path="../data/feed/combined_eng.jsonl")
    feed = "../data/feed/combined_eng.jsonl"
    feed_df = DataCleaner.load_data(feed)
    feed_cleaner = DataCleaner(feed_df)
    feed_cleaner.filter_columns(
        columns_to_keep=["Summary_minimal", "full_text_minimal"]
    )
    feed_cleaner.save_df(save_path="../data/feed/ready_to_feed_eng.jsonl")
    pass


if __name__ == "__main__":
    main()
