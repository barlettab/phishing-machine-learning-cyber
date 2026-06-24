import pandas as pd
import os
from collections import Counter

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RAW_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "datasets",
    "raw",
    "majestic_million.csv"
)

OUTPUT_DIR = os.path.join("ml", "datasets", "processed", "eda")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def main():

    print_section("LOADING DATASET")

    df = pd.read_csv(RAW_PATH)

    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())

    print_section("MISSING VALUES")

    print(df.isnull().sum())

    print_section("BASIC CLEAN OVERVIEW")

    print(f"Unique domains: {df['Domain'].nunique()}")
    print(f"Duplicated domains: {df['Domain'].duplicated().sum()}")

    print_section("TOP TLDs")

    tld_counts = df["TLD"].value_counts().head(20)
    print(tld_counts)

    tld_counts.to_csv(
        os.path.join(OUTPUT_DIR, "top_tlds.csv")
    )

    print_section("GLOBAL RANK STATS")

    print(df["GlobalRank"].describe())

    print_section("REF IPS STATS")

    print(df["RefIPs"].describe())

    print_section("REF SUBNETS STATS")

    print(df["RefSubNets"].describe())

    print_section("DOMAIN SAMPLE")

    print(df["Domain"].head(20).tolist())

    print_section("FILTERING CANDIDATES")

    # heurística simples para ver qualidade do dataset
    high_quality = df[
        (df["RefIPs"] >= 10) &
        (df["RefSubNets"] >= 5)
    ]

    print(f"High quality candidates: {len(high_quality)}")

    high_quality[["Domain", "GlobalRank", "RefIPs", "RefSubNets"]].head(50).to_csv(
        os.path.join(OUTPUT_DIR, "high_quality_domains_sample.csv"),
        index=False
    )

    print_section("SUMMARY")

    print(f"""
Total domains: {len(df)}
High quality domains (heuristic): {len(high_quality)}

Recommendation:
- Use GlobalRank top slice (ex: top 100k)
- Filter RefIPs >= 10
- Filter RefSubNets >= 5
""")


if __name__ == "__main__":
    main()
