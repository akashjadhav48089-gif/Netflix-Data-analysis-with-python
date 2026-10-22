"""Netflix catalog exploratory analysis.

Expected input: data/OTT_Movies.csv
Outputs: outputs/*.csv and outputs/charts/*.png
"""
from pathlib import Path
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "OTT_Movies.csv"
OUTPUTS = ROOT / "outputs"
CHARTS = OUTPUTS / "charts"

REQUIRED_COLUMNS = {
    "show_id", "type", "title", "country", "date_added",
    "release_year", "rating", "duration", "listed_in"
}

def save_bar(series, title, xlabel, ylabel, filename, horizontal=False):
    plt.figure(figsize=(10, 6))
    if horizontal:
        sns.barplot(x=series.values, y=series.index)
    else:
        sns.barplot(x=series.index.astype(str), y=series.values)
        plt.xticks(rotation=35, ha="right")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(CHARTS / filename, dpi=160, bbox_inches="tight")
    plt.close()

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place the permitted CSV at data/OTT_Movies.csv. "
            "See README.md for details."
        )

    OUTPUTS.mkdir(exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    df = pd.read_csv(DATA_PATH)
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")

    # Basic data-quality profile
    quality = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percent": (df.isna().mean() * 100).round(2),
        "unique_values": df.nunique(dropna=True),
    })
    quality.to_csv(OUTPUTS / "data_quality_profile.csv")
    pd.DataFrame([{
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_show_ids": int(df["show_id"].duplicated().sum()),
    }]).to_csv(OUTPUTS / "dataset_overview.csv", index=False)

    # Clean selected text fields and parse dates without silently crashing on bad values.
    for col in ["type", "title", "country", "rating", "duration", "listed_in"]:
        if col in df:
            df[col] = df[col].astype("string").str.strip()
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month_name()

    # Movie vs TV show
    type_counts = df["type"].value_counts(dropna=False).rename_axis("type").reset_index(name="title_count")
    type_counts.to_csv(OUTPUTS / "content_type_counts.csv", index=False)
    save_bar(type_counts.set_index("type")["title_count"], "Catalog by content type",
             "Content type", "Number of titles", "content_type_counts.png")

    # Country mentions: one title may list several countries.
    countries = df[["show_id", "country"]].dropna().copy()
    countries["country"] = countries["country"].str.split(", ")
    countries = countries.explode("country")
    countries["country"] = countries["country"].str.strip()
    countries = countries[countries["country"].ne("") & countries["country"].ne("Unknown")]
    country_counts = countries["country"].value_counts().head(15).rename_axis("country").reset_index(name="title_country_mentions")
    country_counts.to_csv(OUTPUTS / "top_countries.csv", index=False)
    if not country_counts.empty:
        save_bar(country_counts.set_index("country")["title_country_mentions"],
                 "Top 15 countries by catalog mentions", "Title-country mentions",
                 "Country", "top_countries.png", horizontal=True)

    # Genre mentions: a title can have more than one genre.
    genres = df[["show_id", "listed_in"]].dropna().copy()
    genres["genre"] = genres["listed_in"].str.split(", ")
    genres = genres.explode("genre")
    genres["genre"] = genres["genre"].str.strip()
    genre_counts = genres["genre"].value_counts().rename_axis("genre").reset_index(name="title_genre_mentions")
    genre_counts.to_csv(OUTPUTS / "genre_counts.csv", index=False)
    if not genre_counts.empty:
        save_bar(genre_counts.head(15).set_index("genre")["title_genre_mentions"],
                 "Most common genres", "Title-genre mentions", "Genre",
                 "top_genres.png", horizontal=True)

    # Catalog additions by year and month
    additions_year = df["year_added"].dropna().astype(int).value_counts().sort_index()
    additions_year.rename_axis("year_added").reset_index(name="titles_added").to_csv(
        OUTPUTS / "additions_by_year.csv", index=False
    )
    if not additions_year.empty:
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=additions_year.index, y=additions_year.values, marker="o")
        plt.title("Catalog additions by year")
        plt.xlabel("Year added")
        plt.ylabel("Number of titles")
        plt.tight_layout()
        plt.savefig(CHARTS / "additions_by_year.png", dpi=160, bbox_inches="tight")
        plt.close()

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    additions_month = df["month_added"].value_counts().reindex(month_order, fill_value=0)
    additions_month.rename_axis("month_added").reset_index(name="titles_added").to_csv(
        OUTPUTS / "additions_by_month.csv", index=False
    )
    save_bar(additions_month, "Catalog additions by month", "Month",
             "Number of titles", "additions_by_month.png")

    # Ratings
    rating_counts = df["rating"].fillna("Unknown").value_counts().rename_axis("rating").reset_index(name="title_count")
    rating_counts.to_csv(OUTPUTS / "rating_counts.csv", index=False)
    save_bar(rating_counts.head(10).set_index("rating")["title_count"], "Most common content ratings",
             "Rating", "Number of titles", "rating_counts.png", horizontal=True)

    # Movie runtimes; only parse values that look like minutes.
    movies = df.loc[df["type"].eq("Movie"), ["show_id", "title", "duration"]].copy()
    movies["duration_minutes"] = pd.to_numeric(
        movies["duration"].astype("string").str.extract(r"^\s*(\d+)\s*min\s*$", expand=False),
        errors="coerce"
    )
    runtime_summary = movies["duration_minutes"].describe().to_frame("duration_minutes").round(2)
    runtime_summary.to_csv(OUTPUTS / "movie_runtime_summary.csv")
    runtimes = movies["duration_minutes"].dropna()
    if not runtimes.empty:
        plt.figure(figsize=(10, 5))
        sns.histplot(runtimes, bins=25, kde=True)
        plt.title("Distribution of movie runtimes")
        plt.xlabel("Runtime (minutes)")
        plt.ylabel("Number of movies")
        plt.tight_layout()
        plt.savefig(CHARTS / "movie_runtime_distribution.png", dpi=160, bbox_inches="tight")
        plt.close()

    print(f"Loaded {len(df):,} rows and {len(df.columns):,} columns.")
    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print("\nContent type counts:\n", type_counts.to_string(index=False))
    print("\nTop 10 country mentions:\n", country_counts.head(10).to_string(index=False))
    print("\nTop 10 genres:\n", genre_counts.head(10).to_string(index=False))
    print("\nCatalog additions by month:\n", additions_month.to_string())
    print(f"\nOutputs saved under: {OUTPUTS}")

if __name__ == "__main__":
    main()
