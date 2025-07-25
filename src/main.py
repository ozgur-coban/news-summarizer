import pandas as pd

from preprocessing import (
    TurkishPreprocessor,
    DataCleaner,
    DataCombiner,
    EnglishPreprocessor,
)
from scraping import (
    AA_NewsMetadataFetcher,
    AA_ArticleBodyFetcher,
    AA_EnglishNewsMetadataFetcher,
    AA_EnglishArticleBodyFetcher,
)
from eda import Analyzer, TextAnalyzer


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
    # for i in [5, 12, 13, 17]:
    #     fetcher = AA_EnglishNewsMetadataFetcher(
    #         start_page=1,
    #         max_pages=300,  # 3 x 100 = 300 news
    #         category_id=i,  # "World" (choose as you want)
    #         keyword="* * *",  # for all news
    #         save_to_file=True,
    #         save_file_path=f"../data/raw/metadata/metadata_21-7-2025_eng{+i}.jsonl",
    #         is_inplace=True,
    #         page_size=20,  # up to 100
    #     )
    #     fetcher.run()
    # combiner = DataCombiner(
    #     metadata_file="../data/raw/metadata/metadata_17-7-2025_eng.jsonl",
    #     body_file="../data/raw/metadata/metadata_21-7-2025_eng2-3-5-6-8-12-13-17.jsonl",
    # )
    # combiner.run(
    #     "../data/raw/metadata/metadata_21-7-2025_eng.jsonl",
    #     join_type="union",
    # )

    # for title, link in fetcher.results:
    #     print(f"- {title}\n  {link}")

    # body_fetcher = AAArticleBodyFetcher(
    #     metadata_path="../data/raw/metadata/metadata_gundem_13-7-2025_copy.json",
    #     output_path="../data/raw/body/gundem_13-7-2025_body.jsonl",
    # )
    # body_fetcher.run(start=1, end=999)

    # body_fetcher = AA_EnglishArticleBodyFetcher(
    #     metadata_path="../data/raw/metadata/metadata_21-7-2025_eng.jsonl",
    #     output_path="../data/raw/body/full_articles/aa_eng_full_articles_52000.jsonl",
    # )
    # body_fetcher.run(start=1)
    # df_1 = DataCombiner.load_data(
    #     "../data/raw/body/full_articles/aa_eng_full_articles_13000-26000.jsonl"
    # )
    # df_2 = DataCombiner.load_data(
    #     "../data/raw/body/full_articles/aa_eng_full_articles_39000-52000.jsonl"
    # )
    # df_combined = DataCombiner.join_df_union(df_1=df_1, df_2=df_2)
    # DataCombiner.save(
    #     df_combined,
    #     path="../data/raw/body/full_articles/aa_full_articles_21-7-2025_eng.jsonl",
    # )
    # metadata = "../data/raw/metadata/english_news_metadata_17-7-2025.jsonl"
    # body = "../src/tests/output_no_duplicates.jsonl"
    # metadata_df = DataCleaner.load_data(
    #     "../data/raw/metadata/metadata_21-7-2025_eng.jsonl"
    # )
    # body_df = DataCleaner.load_data(
    #     "../data/processed/combined/22-7-2025_eng_eda.jsonl"
    # )
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
    # metadata_cleaner.save_df(
    #     save_path="../data/raw/filtered/metadata_21-7-2025_eng.jsonl"
    # )
    # body_cleaner.filter_columns(
    #     columns_to_keep=[
    #         "Id",
    #         "CreateDateString",
    #         "Title_x",
    #         "Summary",
    #         "Tags",
    #         "Categories",
    #         "full_text",
    #     ]
    # )
    # body_cleaner.drop_missing()
    # body_cleaner.standardize_fields()
    # # body_cleaner.clean_english_articles()
    # body_cleaner.save_df(
    #     save_path="../data/processed/combined/22-7-2025_eda_filtered_eng.jsonl"
    # )
    # prep = TurkishNLTKPreprocessor(path="./metadata.jsonl")
    # prep.load_data()
    # prep.minimal_preprocess_column(column="Summary")
    # prep.save(out_path="../data/feed/clean_metadata.jsonl")
    # prep = TurkishNLTKPreprocessor(path="./body.jsonl")
    # prep.load_data()
    # prep.minimal_preprocess_column("full_text")
    # prep.save(out_path="../data/feed/clean_body.jsonl")
    # prep = EnglishPreprocessor(path="../data/raw/filtered/metadata_21-7-2025_eng.jsonl")
    # prep.load_data()
    # prep.minimal_preprocess_column("Summary")
    # prep.save(out_path="../data/processed/metadata/metadata_21-7-2025_eng.jsonl")
    # prep = EnglishPreprocessor(
    #     path="../data/raw/filtered/aa_full_articles_21-7-2025_eng.jsonl"
    # )
    # prep.load_data()
    # prep.minimal_preprocess_column("full_text")
    # prep.save(out_path="../data/processed/body/aa_full_articles_21-7-2025_eng.jsonl")
    # prep = EnglishPreprocessor(
    #     path="../data/processed/combined/22-7-2025_eda_filtered_preprocessed_eng.jsonl"
    # )
    # prep.load_data()
    # prep.normalize_column(column="Tags", new_column="tags_norm")
    # prep.save(
    #     out_path="../data/processed/combined/22-7-2025_eda_filtered_preprocessed_eng.jsonl"
    # )

    # combiner = DataCombiner(
    #     metadata_file="../data/processed/combined/21-7-2025_eng.jsonl",
    #     body_file="../data/processed/combined/combined_eng.jsonl",
    # )
    # combiner.run(
    #     path="../data/processed/combined/21-7-2025_eng_2.jsonl", join_type="union"
    # )

    # feed_df = DataCleaner.load_data("../data/processed/combined/21-7-2025_eng_2.jsonl")
    # feed_cleaner = DataCleaner(feed_df)
    # feed_cleaner.filter_columns(
    #     columns_to_keep=["Summary_minimal", "full_text_minimal"]
    # )
    # feed_cleaner.save_df(save_path="../data/feed/ready_to_feed_21-7-2025_eng_2.jsonl")
    # ! EDA
    # analyzer = Analyzer(
    #     source_file="../data/eda/22-7-2025_eda_filtered_preprocessed_eng.jsonl"
    # )
    # analyzer.plot_tag_counts(col="tags_norm")
    # analyzer.articles_per_day(print_bool=True)
    # analyzer.longest_shortest_day()
    # analyzer.articles_per_month_around_date(selected_date="2024-06-20")
    # analyzer.plot_trend(freq="M")
    #
    # counter = analyzer.get_tag_counts(col="tags_norm")
    # most_common_tags = [x[0] for x in counter.most_common(5)]
    # analyzer.plot_tag_coverage_over_time(tag=most_common_tags[4], tags_col="tags_norm")
    #
    # analyzer.tag_cooccurrence_matrix(tag_col="tags_norm")
    #
    # mtx = analyzer.get_tag_month_matrix(tag_col="tags_norm", date_col="date")
    # Analyzer.plot_tag_temporal_shifts(mtx)
    # #
    # #
    # emergence_df = analyzer.topic_emergence_decay(
    #     tag_col="tags_norm", date_col="date", freq="M", min_window_count=2
    # )
    # print(
    #     emergence_df[
    #         ["window", "n_emergent", "emergent_tags", "n_decayed", "decayed_tags"]
    #     ].tail(8)
    # )
    # Analyzer.plot_topic_emergence_decay(emergence_df=emergence_df)

    # analyzer.plot_article_velocity_agg(
    #     "Gaza", tag_col="tags_norm", date_col="date", time_unit="days", freq="M"
    # )
    # #
    # grouped, first, peak, last = analyzer.event_coverage_lifespan(
    #     "Gaza", tag_col="tags_norm", date_col="date", freq="M"
    # )
    # if grouped is not None:
    #     Analyzer.plot_event_lifespan(grouped, first, peak, last, freq="M", tag="Gaza")
    #

    # text_analyzer = TextAnalyzer(
    #     source_file="../data/eda/22-7-2025_eda_filtered_preprocessed_eng.jsonl",
    #     title_col="title",
    # )
    # text_analyzer.df.rename(columns={"Title_x": "title"}, inplace=True)
    # text_analyzer.df.rename(columns={"Summary": "summary"}, inplace=True)
    # TextAnalyzer._calculate_word_count(
    #     df=text_analyzer.df, text_col="title", new_col="n_words_title"
    # )
    # TextAnalyzer._calculate_word_count(
    #     df=text_analyzer.df, text_col="summary", new_col="n_words_summary"
    # )
    # TextAnalyzer._calculate_word_count(
    #     df=text_analyzer.df, text_col="full_text", new_col="n_words_full_text"
    # )

    # # text_analyzer.df.drop("n_words", axis=1, inplace=True)
    # DataCombiner.save(
    #     df=text_analyzer.df,
    #     path="../data/eda/22-7-2025_eda_filtered_preprocessed_eng.jsonl",
    # )
    # text_analyzer.length_stats(text_col="full_text_norm")
    # text_analyzer.length_hist(text_col="full_text_norm")
    # text_analyzer.most_common_words(text_col="full_text_norm", ngram=4, n=30)

    pass


if __name__ == "__main__":
    main()
