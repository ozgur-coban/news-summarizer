import requests
import random
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup


class NewsDownloader:
    def __init__(self):
        self.api_url = "https://www.aa.com.tr/tr/gundem"  # POST for scrolling
        self.base_url = "https://www.aa.com.tr/tr/gundem"  # GET for static top
        self.today = datetime.today().strftime("%d.%m.%Y")
        self.articles = []

        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://www.aa.com.tr/tr/gundem",
            "Origin": "https://www.aa.com.tr",
        }

    def fetch_batch(self, start, batch_size):
        data = {"numFirst": start, "numFin": start + batch_size}

        try:
            resp = requests.post(
                self.api_url,
                headers=self.headers,
                data=data,
                timeout=15,
            )

            print("✅ Status:", resp.status_code)
            print("✅ Content-Type:", resp.headers.get("Content-Type", ""))

            resp.raise_for_status()

            if "application/json" in resp.headers.get("Content-Type", ""):
                return resp.json()
            else:
                print("❌ Not JSON response.")
                print("🧪 Response preview:", resp.text[:300])
                return []

        except requests.exceptions.Timeout:
            print("❌ Request timed out.")
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []

    def fetch_all_until_today(self, batch_size=5, delay=5):
        all_articles = []
        # to not get an retrieval error
        start = 5

        print(f"📅 Today: {self.today}")
        while True:
            batch = self.fetch_batch(start, batch_size)

            if not batch:
                print(f"⛔ No articles found at batch starting from {start}. Stopping.")
                break

            # Filter only today's articles
            todays_batch = [
                article for article in batch if article.get("StartDate") == self.today
            ]

            if not todays_batch:
                print(
                    f"⏹️ No more articles from today at batch starting from {start}. Done."
                )
                break

            print(
                f"✅ Batch {start} → Retrieved {len(todays_batch)} articles from today."
            )
            all_articles.extend(todays_batch)

            # Prepare for next loop
            start += batch_size
            sleep(delay + random.uniform(0, 1.5))
            for article in all_articles:
                if "Route" in article and "ID" in article:
                    article["URL"] = (
                        f"https://www.aa.com.tr/tr/gundem/{article['Route']}/{article['ID']}"
                    )

        return all_articles[2:]

    def scrape_initial_page(self):
        try:
            html = requests.get(self.base_url, headers=self.headers).text
            soup = BeautifulSoup(html, "html.parser")
            articles = []

            def extract_article(tag, selector):
                title_tag = tag.select_one(selector)
                link_tag = tag.find("a", href=True)
                return {
                    "Title": title_tag.get_text(strip=True) if title_tag else "",
                    "URL": "https://www.aa.com.tr" + link_tag["href"]
                    if link_tag
                    else "",
                }

            # Top banner article
            top_container = soup.select_one(".konu-ust-icerik.container")
            if top_container:
                article = extract_article(top_container, "h2 a")
                if article["Title"]:
                    articles.append(article)

            # Two side articles
            for tag in soup.select(".konu-ust-manset"):
                article = extract_article(tag, "h2 span.category-beyaz-manset")
                if article["Title"]:
                    articles.append(article)

            # Four lower grid items
            for tag in soup.select(".konu-ust-mansetalti .col-sm-6"):
                article = extract_article(tag, "h4")
                if article["Title"]:
                    articles.append(article)
            # return [{"Title":'title',"URL":'url'}]
            return articles

        except Exception as e:
            print(f"❌ Failed to scrape initial page: {e}")
            return []
