from preprocessing import Preprocessor
from scraping import TagExtractor
from eda import TagAnalyzer


def main():
    pre = Preprocessor()
    extractor = TagExtractor(html_dir="../data/raw/html_articles", preprocessor=pre)

    extractor.process_all_files().save_to_csv("../data/processed/temp_tags.csv")
    tag_analyzer = TagAnalyzer(source_file="../data/processed/temp_tags.csv")
    tag_analyzer.process_topic_counts(output_path="../data/processed/tags.csv")


if __name__ == "__main__":
    main()
