"""
Week 9 - Data Pipeline
Model Retraining Stage
"""

import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    classification_report
)


DATA_FOLDER = "data"
MODEL_FOLDER = "models"
OUTPUT_FOLDER = "output"


TRAIN_FILE = os.path.join(
    DATA_FOLDER,
    "training_data.csv"
)

MODEL_FILE = os.path.join(
    MODEL_FOLDER,
    "sentiment_model.pkl"
)

VECTORIZER_FILE = os.path.join(
    MODEL_FOLDER,
    "count_vectorizer.pkl"
)

REPORT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "training_report.txt"
)


def train_model():

    print(
        "\nStarting model retraining..."
    )

    if not os.path.exists(
        TRAIN_FILE
    ):

        raise FileNotFoundError(
            f"Training dataset not found: "
            f"{TRAIN_FILE}"
        )

    df = pd.read_csv(
        TRAIN_FILE
    )

    required_columns = [
        "text",
        "sentiment"
    ]

    for column in required_columns:

        if column not in df.columns:

            raise ValueError(
                f"Missing column: {column}"
            )

    df = df.dropna(
        subset=required_columns
    )

    X = df["text"].astype(str)

    y = df["sentiment"].astype(str)

    vectorizer = CountVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2)
    )

    X_vectorized = vectorizer.fit_transform(
        X
    )

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X_vectorized,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )

    model = MultinomialNB()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    report = classification_report(
        y_test,
        predictions,
        zero_division=0
    )

    os.makedirs(
        MODEL_FOLDER,
        exist_ok=True
    )

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_FILE
    )

    joblib.dump(
        vectorizer,
        VECTORIZER_FILE
    )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "WEEK 9 MODEL RETRAINING REPORT\n"
        )

        file.write(
            "=" * 50 + "\n\n"
        )

        file.write(
            f"Training Records: {len(df)}\n"
        )

        file.write(
            f"Accuracy: {accuracy:.4f}\n\n"
        )

        file.write(
            "Classification Report\n"
        )

        file.write(
            report
        )

    print(
        f"Model saved: {MODEL_FILE}"
    )

    print(
        f"Vectorizer saved: {VECTORIZER_FILE}"
    )

    print(
        f"Accuracy: {accuracy:.4f}"
    )

    print(
        "Retraining completed successfully."
    )


if __name__ == "__main__":

    train_model()