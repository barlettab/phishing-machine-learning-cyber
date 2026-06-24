import pandas as pd
import os
import re

# =========================
# CONFIG
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

RAW_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "datasets",
    "raw",
    "majestic_million.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "datasets",
    "processed",
    "domains.csv"
)

TOP_N = 20000  # ajuste aqui (20k recomendado)

# =========================
# DOMAIN FILTERS
# =========================

BLACKLIST_PATTERNS = [
    r"googleapis",
    r"gstatic",
    r"doubleclick",
    r"googletagmanager",
    r"google-analytics",
    r"facebook\.net",
    r"amazon-adsystem",
    r"cdn\.",
    r"static",
    r"assets",
    r"fonts",
    r"api\.",
    r"analytics",
    r"adservice",
    r"tracking"
]

BLACKLIST_REGEX = re.compile("|".join(BLACKLIST_PATTERNS))


# =========================
# FUNCTIONS
# =========================

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def is_valid_domain(domain: str) -> bool:
    if pd.isna(domain):
        return False

    domain = domain.lower().strip()

    # remove obvious garbage
    if domain.startswith("xn--"):
        return False

    if BLACKLIST_REGEX.search(domain):
        return False

    # basic sanity check
    if len(domain) < 4 or "." not in domain:
        return False

    return True


# =========================
# MAIN PIPELINE
# =========================

def main():

    print_section("LOADING DATASET")

    df = pd.read_csv(RAW_PATH)

    print(f"Original size: {df.shape}")

    print_section("SORTING BY GLOBAL RANK")

    df = df.sort_values("GlobalRank", ascending=True)

    df_top = df.head(TOP_N)

    print(f"After TOP_N ({TOP_N}): {df_top.shape}")

    print_section("CLEANING DOMAINS")

    df_top["Domain"] = df_top["Domain"].str.lower()

    df_clean = df_top[df_top["Domain"].apply(is_valid_domain)]

    print(f"After filtering: {df_clean.shape}")

    removed = len(df_top) - len(df_clean)

    print(f"Removed domains: {removed}")

    print_section("FINAL STATS")

    print(f"Final domains: {len(df_clean)}")

    print("\nTop TLDs after cleaning:")
    print(df_clean["TLD"].value_counts().head(10))

    print("\nSample domains:")
    print(df_clean["Domain"].head(20).tolist())

    print_section("EXPORTING")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df_clean[["Domain"]].to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Saved to: {OUTPUT_PATH}")

    print_section("DONE")


if __name__ == "__main__":
    main()