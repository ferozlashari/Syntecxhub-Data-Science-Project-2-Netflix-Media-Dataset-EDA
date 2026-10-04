"""
netflix_analysis.py
--------------------
Project 2 — Netflix / Media Dataset EDA.
Covers: counts by type, year trends, top genres, content growth over
time, runtime distributions, top-10 lists, and an exported summary.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

sns.set_theme(style="whitegrid")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "netflix_titles.csv"
CHARTS_DIR = BASE_DIR.parent / "static" / "charts" / "netflix"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = ["#4b2e83", "#cf8fe0"]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, parse_dates=["date_added"])
    return df


def explode_genres(df: pd.DataFrame) -> pd.Series:
    all_genres = df["listed_in"].str.split(", ").explode()
    return all_genres


def extract_runtime_minutes(df: pd.DataFrame) -> pd.Series:
    movies = df[df["type"] == "Movie"].copy()
    movies["minutes"] = movies["duration"].str.extract(r"(\d+)").astype(float)
    return movies["minutes"]


def run() -> dict:
    df = load_data()
    n = len(df)

    # --- Chart 1: Counts by type (bar + pie combined as two charts) ---
    type_counts = df["type"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(type_counts.index, type_counts.values, color=PALETTE)
    ax.set_title("Titles by Content Type", fontsize=14, fontweight="bold")
    ax.set_ylabel("Count")
    for i, v in enumerate(type_counts.values):
        ax.text(i, v + 20, f"{v:,}", ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "type_counts.png", dpi=130)
    plt.close(fig)

    # --- Chart 2: Year trend — titles released per year (last 15 years) ---
    year_counts = df["release_year"].value_counts().sort_index()
    recent = year_counts[year_counts.index >= year_counts.index.max() - 14]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(recent.index, recent.values, marker="o", color="#4b2e83", linewidth=2)
    ax.set_title("Titles Released by Year (last 15 years)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Number of Titles")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "year_trend.png", dpi=130)
    plt.close(fig)

    # --- Chart 3: Content growth over time — cumulative titles added ---
    added_by_month = df.set_index("date_added").resample("ME").size()
    cumulative = added_by_month.cumsum()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(cumulative.index, cumulative.values, color="#7b5ea7", linewidth=2.2)
    ax.fill_between(cumulative.index, cumulative.values, color="#cf8fe0", alpha=0.25)
    ax.set_title("Cumulative Catalog Growth Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date Added")
    ax.set_ylabel("Cumulative Titles")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "catalog_growth.png", dpi=130)
    plt.close(fig)

    # --- Chart 4: Top 10 genres (bar) ---
    genre_counts = explode_genres(df).value_counts().head(10)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(genre_counts.index[::-1], genre_counts.values[::-1], color="#9b7fd4")
    ax.set_title("Top 10 Genres", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Titles")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "top_genres.png", dpi=130)
    plt.close(fig)

    # --- Chart 5: Runtime distribution (movies, histogram) ---
    minutes = extract_runtime_minutes(df).dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(minutes, bins=35, kde=True, color="#8a6fce", ax=ax)
    ax.axvline(minutes.median(), color="#2e1a52", linestyle="--", linewidth=1.5,
               label=f"Median: {minutes.median():.0f} min")
    ax.set_title("Movie Runtime Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Runtime (minutes)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "runtime_distribution.png", dpi=130)
    plt.close(fig)

    # --- Top-10 lists ---
    top_genres_list = genre_counts.head(10).to_dict()
    top_years_list = df["release_year"].value_counts().head(10).to_dict()
    top_countries_list = df["country"].value_counts().head(10).to_dict()

    movie_pct = type_counts.get("Movie", 0) / n * 100
    tv_pct = type_counts.get("TV Show", 0) / n * 100
    peak_year = int(year_counts.idxmax())
    top_genre = genre_counts.index[0]
    growth_last_2y = cumulative.iloc[-1] - cumulative.iloc[max(0, len(cumulative) - 25)]

    summary = (
        f"The catalog contains {n:,} titles: {movie_pct:.0f}% Movies and {tv_pct:.0f}% TV Shows. "
        f"Content releases peaked in {peak_year} with {int(year_counts.max())} titles, reflecting "
        f"the general industry-wide surge in streaming-original content in recent years. "
        f"'{top_genre}' is the most common genre tag ({int(genre_counts.iloc[0])} titles), and the "
        f"catalog grew by roughly {int(growth_last_2y):,} titles in the most recent 24 months of "
        f"additions alone — most of the library's growth is recent rather than evenly spread "
        f"across the catalog's history. Movie runtimes cluster around a median of "
        f"{minutes.median():.0f} minutes with a fairly normal spread, typical of mainstream "
        f"feature-length films, while a long tail extends past 180 minutes for a small number "
        f"of titles. A line chart was used for the year trend and cumulative growth since both "
        f"are continuous-over-time measures, while genres and content type — categorical counts — "
        f"are shown as bar charts for precise ranking."
    )

    return {
        "charts": [
            "type_counts.png", "year_trend.png", "catalog_growth.png",
            "top_genres.png", "runtime_distribution.png",
        ],
        "top_10_genres": top_genres_list,
        "top_10_years": {str(k): v for k, v in top_years_list.items()},
        "top_10_countries": top_countries_list,
        "summary": summary,
        "row_count": n,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, default=str))
