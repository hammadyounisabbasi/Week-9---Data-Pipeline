"""
Week 9 - Data Pipeline
Scraping Stage

Scrapes quotes from QuotesToScrape.com
and saves them as raw_posts.csv.
"""

import os
import requests
import pandas as pd

from bs4 import BeautifulSoup


DATA_FOLDER = "data"
RAW_FILE = os.path.join(
    DATA_FOLDER,
    "raw_posts.csv"
)

BASE_URL = "https://quotes.toscrape.com/page/{}/"


def scrape_quotes():

    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )

    records = []

    page = 1

    while True:

        url = BASE_URL.format(page)

        print(f"Scraping page {page}...")

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

        except requests.RequestException as error:

            print(
                f"Scraping error: {error}"
            )

            break

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        quotes = soup.find_all(
            "div",
            class_="quote"
        )

        if not quotes:

            break

        for quote in quotes:

            text = quote.find(
                "span",
                class_="text"
            )

            author = quote.find(
                "small",
                class_="author"
            )

            if text and author:

                records.append({
                    "text": text.get_text(
                        strip=True
                    ),
                    "author": author.get_text(
                        strip=True
                    )
                })

        page += 1

    df = pd.DataFrame(records)

    df.drop_duplicates(
        subset=["text"],
        inplace=True
    )

    df.to_csv(
        RAW_FILE,
        index=False
    )

    print(
        f"Raw dataset saved: {RAW_FILE}"
    )

    print(
        f"Total records: {len(df)}"
    )


if __name__ == "__main__":

    scrape_quotes()