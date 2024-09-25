import pandas as pd
import requests
import os
from dotenv import load_dotenv
from trakt_scraper import create_watched_movies_csv

# Load environment variables
load_dotenv(dotenv_path=".env")

# TMDb API configuration
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def get_movie_details(tmdb_id):
    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None


def main():
    # First, update the watched_movies.csv file
    create_watched_movies_csv()

    # Read the existing CSV file
    try:
        df = pd.read_csv("data/watched_movies.csv")
    except FileNotFoundError:
        print("Error: The file 'data/watched_movies.csv' was not found.")
        return

    print("CSV file information:")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Number of rows: {len(df)}")
    print("\nFirst 5 rows of the CSV:")
    print(df.head())

    if "TmdbId" not in df.columns:
        print("\nError: 'TmdbId' column not found in the CSV file.")
        print("Available columns are:", df.columns.tolist())
        return

    # Create a list to store new movie details
    new_movies = []

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        tmdb_id = row["TmdbId"]
        movie_details = get_movie_details(tmdb_id)

        if movie_details:
            new_movie = {
                "TmdbId": tmdb_id,
                "Title": movie_details.get("title", ""),
                "Tagline": movie_details.get("tagline", ""),
                "ReleaseDate": movie_details.get("release_date", ""),
                "Runtime": movie_details.get("runtime", ""),
                "Overview": movie_details.get("overview", ""),
                "VoteAverage": movie_details.get("vote_average", ""),
                "VoteCount": movie_details.get("vote_count", ""),
                "Popularity": movie_details.get("popularity", ""),
                "Genres": ", ".join(
                    [genre["name"] for genre in movie_details.get("genres", [])]
                ),
                "ProductionCompanies": ", ".join(
                    [
                        company["name"]
                        for company in movie_details.get("production_companies", [])
                    ]
                ),
                "PosterPath": movie_details.get("poster_path", ""),
                "BackdropPath": movie_details.get("backdrop_path", ""),
            }
            new_movies.append(new_movie)

    # Create a new DataFrame with the scraped data
    new_df = pd.DataFrame(new_movies)

    # Merge the new DataFrame with the existing one
    merged_df = pd.merge(df, new_df, on="TmdbId", how="left", suffixes=("", "_new"))

    # Update existing columns and add new ones
    for col in new_df.columns:
        if col != "TmdbId":
            new_col = col + "_new"
            if new_col in merged_df.columns:
                if col in df.columns:
                    # Update existing column
                    merged_df[col] = merged_df[new_col].fillna(merged_df[col])
                else:
                    # Add new column
                    merged_df[col] = merged_df[new_col]
                merged_df.drop(new_col, axis=1, inplace=True)

    # Reorder columns
    desired_order = [
        "Title",
        "Year",
        "WatchedAt",
        "Plays",
        "Tagline",
        "ReleaseDate",
        "Runtime",
        "Overview",
        "VoteAverage",
        "VoteCount",
        "Popularity",
        "Genres",
        "ProductionCompanies",
        "Slug",
        "TraktId",
        "ImdbId",
        "TmdbId",
        "PosterPath",
        "BackdropPath",
    ]

    # Ensure all desired columns exist, add empty ones if missing
    for col in desired_order:
        if col not in merged_df.columns:
            merged_df[col] = ""

    # Reorder the columns
    merged_df = merged_df[desired_order]

    # Save the updated DataFrame to a new CSV file
    merged_df.to_csv("data/updated_watched_movies.csv", index=False)
    print("Updated data saved to 'data/updated_watched_movies.csv'")

    print("\nUpdated CSV file information:")
    print(f"Columns: {merged_df.columns.tolist()}")
    print(f"Number of rows: {len(merged_df)}")
    print("\nFirst 5 rows of the updated CSV:")
    print(merged_df.head())


if __name__ == "__main__":
    main()
