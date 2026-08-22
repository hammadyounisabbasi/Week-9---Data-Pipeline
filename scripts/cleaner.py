"""
Week 9 - Data Pipeline
Cleaning Stage
"""

import os
import re
import pandas as pd


DATA_FOLDER = "data"

RAW_FILE = os.path.join(
    DATA_FOLDER,
    "raw_posts.csv"
)

CLEAN_FILE = os.path.join(
    DATA_FOLDER,
    "cleaned_posts.csv"
)


def clean_text(text):

    text = str(text)

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    # Remove HTML
    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    # Remove numbers
    text = re.sub(
        r"\d+",
        "",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def clean_dataset():

    if not os.path.exists(
        RAW_FILE
    ):

        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_FILE}"
        )

    df = pd.read_csv(
        RAW_FILE
    )

    df["clean_text"] = (
        df["text"]
        .apply(clean_text)
    )

    df.dropna(
        subset=["clean_text"],
        inplace=True
    )

    df.drop_duplicates(
        subset=["clean_text"],
        inplace=True
    )

    df = df[
        df["clean_text"].str.len() > 5
    ]

    df.to_csv(
        CLEAN_FILE,
        index=False
    )

    print(
        f"Clean dataset saved: {CLEAN_FILE}"
    )

    print(
        f"Clean records: {len(df)}"
    )


if __name__ == "__main__":

    clean_dataset()