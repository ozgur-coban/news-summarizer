from preprocessing import Preprocessor
from scraping import TopicExtractor


def main():
    pre = Preprocessor()
    extractor = TopicExtractor(html_dir="../data/raw/html_articles", preprocessor=pre)

    extractor.process_all_files().save_to_csv("../data/processed/topics.csv")


if __name__ == "__main__":
    main()
