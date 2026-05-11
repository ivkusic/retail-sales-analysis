import os
import urllib.request
import pandas as pd

DATA_URL = (
    "https://raw.githubusercontent.com/leonism/sample-superstore"
    "/master/data/superstore.csv"
)
RAW_PATH = os.path.join("data", "superstore_raw.csv")
CLEAN_PATH = os.path.join("data", "superstore_clean.csv")


def download_data(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    urllib.request.urlretrieve(url, dest)


def load_data(path):
    df = pd.read_csv(path, encoding="utf-8")
    print(f"Loaded {len(df):,} rows and {df.shape[1]} columns.")
    return df


def inspect_data(df):
    null_counts = df.isnull().sum()
    print("Nulls:\n", null_counts[null_counts > 0] if null_counts.sum() > 0 else "None")
    print(f"Duplicates: {df.duplicated().sum():,}")


def clean_data(df):
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")

    df["Profit Margin %"] = df.apply(
        lambda row: (row["Profit"] / row["Sales"] * 100) if row["Sales"] != 0 else 0.0,
        axis=1,
    ).round(2)

    df["Days to Ship"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df = df.drop_duplicates()
    return df


def save_data(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved to: {path} — {df.shape[0]:,} rows × {df.shape[1]} columns")


def main():
    download_data(DATA_URL, RAW_PATH)
    df = load_data(RAW_PATH)
    inspect_data(df)
    df_clean = clean_data(df)
    save_data(df_clean, CLEAN_PATH)


if __name__ == "__main__":
    main()
