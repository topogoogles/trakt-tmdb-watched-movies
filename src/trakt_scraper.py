import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Trakt.tv API configuration
TRAKT_CLIENT_ID = os.getenv("TRAKT_CLIENT_ID")
TRAKT_ACCESS_TOKEN = os.getenv("TRAKT_ACCESS_TOKEN")
TRAKT_API_URL = "https://api.trakt.tv"

headers = {
    "Content-Type": "application/json",
    "trakt-api-version": "2",
    "trakt-api-key": TRAKT_CLIENT_ID,
    "Authorization": f"Bearer {TRAKT_ACCESS_TOKEN}",
}


def get_watched_movies(limit=None):
    url = f"{TRAKT_API_URL}/sync/history/movies"
    params = {"limit": 100, "page": 1}  # Increase limit to 100 items per page
    all_movies = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            movies = response.json()
            if not movies:
                break  # No more movies to fetch
            all_movies.extend(movies)
            params["page"] += 1  # Move to the next page
        else:
            print(f"Error: {response.status_code}")
            return None

    return all_movies


def process_watched_movies(movies):
    processed_movies = []
    for movie in movies:
        processed_movie = {
            "TraktId": movie["movie"]["ids"]["trakt"],
            "ImdbId": movie["movie"]["ids"]["imdb"],
            "TmdbId": movie["movie"]["ids"]["tmdb"],
            "Slug": movie["movie"]["ids"]["slug"],
            "Title": movie["movie"]["title"],
            "Year": movie["movie"]["year"],
            "WatchedAt": movie["watched_at"],
            "Plays": 1,  # Initialize play count
        }
        processed_movies.append(processed_movie)
    return processed_movies


def create_watched_movies_csv(output_file="data/watched_movies.csv", limit=None):
    watched_movies = get_watched_movies(limit)
    if watched_movies:
        processed_movies = process_watched_movies(watched_movies)

        # Convert to DataFrame
        df = pd.DataFrame(processed_movies)

        # Group by movie and count plays
        df = (
            df.groupby(["TraktId", "ImdbId", "TmdbId", "Slug", "Title", "Year"])
            .agg(
                {
                    "WatchedAt": "max",  # Get the most recent watch date
                    "Plays": "count",  # Count the number of plays
                }
            )
            .reset_index()
        )

        # Sort by most recently watched
        df = df.sort_values("WatchedAt", ascending=False)

        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"Watched movies data saved to {output_file}")
        print(f"Total movies: {len(df)}")
    else:
        print("Failed to retrieve watched movies data")


if __name__ == "__main__":
    create_watched_movies_csv()
