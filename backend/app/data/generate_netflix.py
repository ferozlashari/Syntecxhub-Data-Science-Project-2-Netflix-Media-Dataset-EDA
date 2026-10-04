"""
generate_netflix.py
--------------------
Builds a synthetic streaming-catalog dataset shaped like the classic
Kaggle "Netflix Titles" dataset (same columns), with realistic patterns:
catalog growth accelerating in recent years, Movies outnumbering TV
Shows, genre popularity skew, and a believable runtime distribution.
No internet access required.
"""

import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(21)

OUT_FILE = Path(__file__).resolve().parent / "netflix_titles.csv"

GENRES = [
    "Dramas", "Comedies", "Action & Adventure", "Documentaries", "Thrillers",
    "Romantic Movies", "International Movies", "Crime TV Shows", "Kids' TV",
    "Sci-Fi & Fantasy", "Horror Movies", "Stand-Up Comedy", "Anime Series",
    "Reality TV", "Sports Movies",
]
GENRE_WEIGHTS = np.array([14, 12, 10, 9, 9, 8, 10, 6, 5, 5, 4, 3, 2, 2, 1], dtype=float)
GENRE_WEIGHTS /= GENRE_WEIGHTS.sum()

COUNTRIES = ["United States", "India", "United Kingdom", "Canada", "Pakistan",
             "South Korea", "Japan", "France", "Nigeria", "Spain"]
COUNTRY_WEIGHTS = np.array([34, 11, 8, 6, 5, 7, 6, 6, 5, 5], dtype=float)
COUNTRY_WEIGHTS /= COUNTRY_WEIGHTS.sum()

RATINGS = ["TV-MA", "TV-14", "R", "PG-13", "TV-PG", "PG", "TV-Y7", "TV-Y", "G"]
RATING_WEIGHTS = np.array([28, 24, 12, 10, 10, 6, 5, 3, 2], dtype=float)
RATING_WEIGHTS /= RATING_WEIGHTS.sum()

TITLE_WORDS_A = ["Shadow", "Silent", "Broken", "Golden", "Last", "Hidden", "Crimson", "Lost",
                  "Midnight", "Eternal", "Secret", "Wild", "Dark", "Rising", "Forgotten"]
TITLE_WORDS_B = ["Kingdom", "Heart", "City", "Legacy", "Journey", "Horizon", "Chronicles",
                  "Dreams", "Storm", "Empire", "Garden", "River", "Code", "Letters", "Flame"]


def random_title():
    return f"{np.random.choice(TITLE_WORDS_A)} {np.random.choice(TITLE_WORDS_B)}"


def generate(n=6000):
    # content type: movies outnumber TV shows, roughly like the real dataset
    content_type = np.random.choice(["Movie", "TV Show"], size=n, p=[0.70, 0.30])

    # release years: long tail back to 1960s, heavy concentration 2015-2026
    recent_years = np.random.choice(np.arange(2015, 2027), size=int(n * 0.75),
                                     p=np.linspace(1, 3, 12) / np.linspace(1, 3, 12).sum())
    older_years = np.random.choice(np.arange(1960, 2015), size=n - len(recent_years))
    release_year = np.concatenate([recent_years, older_years])
    np.random.shuffle(release_year)

    # date_added: catalog growth accelerating, added dates cluster 2018-2026,
    # always on/after release_year
    added_year = np.clip(
        release_year + np.random.exponential(1.5, n).astype(int),
        2015, 2026
    )
    added_month = np.random.randint(1, 13, n)
    added_day = np.random.randint(1, 28, n)
    date_added = pd.to_datetime({
        "year": added_year, "month": added_month, "day": added_day
    }, errors="coerce")

    country = np.random.choice(COUNTRIES, size=n, p=COUNTRY_WEIGHTS)
    rating = np.random.choice(RATINGS, size=n, p=RATING_WEIGHTS)

    # duration: movies in minutes (skewed ~70-150), TV shows in seasons (1-3 typical)
    duration = []
    for t in content_type:
        if t == "Movie":
            mins = int(np.clip(np.random.normal(100, 22), 42, 220))
            duration.append(f"{mins} min")
        else:
            seasons = int(np.clip(np.random.exponential(1.4) + 1, 1, 12))
            duration.append(f"{seasons} Season{'s' if seasons > 1 else ''}")

    # 1-3 genres per title, weighted
    listed_in = []
    for _ in range(n):
        k = np.random.choice([1, 2, 3], p=[0.3, 0.45, 0.25])
        genres = np.random.choice(GENRES, size=k, replace=False, p=GENRE_WEIGHTS)
        listed_in.append(", ".join(genres))

    titles = [random_title() for _ in range(n)]
    show_id = [f"s{i+1}" for i in range(n)]

    df = pd.DataFrame({
        "show_id": show_id,
        "type": content_type,
        "title": titles,
        "country": country,
        "date_added": date_added,
        "release_year": release_year,
        "rating": rating,
        "duration": duration,
        "listed_in": listed_in,
    })
    df = df.dropna(subset=["date_added"]).reset_index(drop=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"Generated {len(df):,} titles -> {OUT_FILE}")
    return df


if __name__ == "__main__":
    generate()
