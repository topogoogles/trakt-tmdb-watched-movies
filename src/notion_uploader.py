import os
import pandas as pd
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime
from notion_client.errors import APIResponseError


# Load environment variables
load_dotenv()

# Notion API configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)


def get_existing_movies():
    existing_movies = {}
    has_more = True
    start_cursor = None

    while has_more:
        response = notion.databases.query(
            database_id=NOTION_DATABASE_ID, start_cursor=start_cursor
        )

        for page in response["results"]:
            tmdb_id = page["properties"]["TmdbId"]["number"]
            existing_movies[tmdb_id] = page["id"]

        has_more = response["has_more"]
        start_cursor = response["next_cursor"]

    return existing_movies


def create_notion_page(row):
    properties = {
        "Title": {"title": [{"text": {"content": row["Title"]}}]},
        "Year": {"number": row["Year"]},
        "WatchedAt": {"date": {"start": row["WatchedAt"]}},
        "Plays": {"number": row["Plays"]},
        "Tagline": {"rich_text": [{"text": {"content": row["Tagline"]}}]},
        "ReleaseDate": {"date": {"start": row["ReleaseDate"]}},
        "Runtime": {"number": row["Runtime"]},
        "Overview": {"rich_text": [{"text": {"content": row["Overview"]}}]},
        "VoteAverage": {"number": row["VoteAverage"]},
        "VoteCount": {"number": row["VoteCount"]},
        "Popularity": {"number": row["Popularity"]},
        "Genres": {
            "multi_select": [
                {"name": genre.strip()}
                for genre in row["Genres"].split(",")
                if genre.strip()
            ]
        },
        "ProductionCompanies": {
            "rich_text": [{"text": {"content": row["ProductionCompanies"]}}]
        },
        "Slug": {"rich_text": [{"text": {"content": row["Slug"]}}]},
        "TraktId": {"number": row["TraktId"]},
        "ImdbId": {"rich_text": [{"text": {"content": row["ImdbId"]}}]},
        "TmdbId": {"number": row["TmdbId"]},
        "PosterPath": {"rich_text": [{"text": {"content": row["PosterPath"]}}]},
        "BackdropPath": {"rich_text": [{"text": {"content": row["BackdropPath"]}}]},
        "BackdropImage": {
            "files": (
                [
                    {
                        "name": "Backdrop",
                        "type": "external",
                        "external": {
                            "url": f"https://image.tmdb.org/t/p/w500{row['BackdropPath']}"
                        },
                    }
                ]
                if pd.notna(row["BackdropPath"])
                else []
            )
        },
    }

    notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID}, properties=properties
    )


def update_notion_page(page_id, row):
    properties = {
        "Title": {"title": [{"text": {"content": row["Title"]}}]},
        "Year": {"number": int(row["Year"]) if pd.notna(row["Year"]) else None},
        "WatchedAt": {
            "date": {"start": row["WatchedAt"]} if pd.notna(row["WatchedAt"]) else None
        },
        "Plays": {"number": int(row["Plays"]) if pd.notna(row["Plays"]) else None},
        "Tagline": {
            "rich_text": [
                {
                    "text": {
                        "content": (
                            str(row["Tagline"])[:2000]
                            if pd.notna(row["Tagline"])
                            else ""
                        )
                    }
                }
            ]
        },
        "ReleaseDate": {
            "date": (
                {"start": row["ReleaseDate"]} if pd.notna(row["ReleaseDate"]) else None
            )
        },
        "Runtime": {
            "number": int(row["Runtime"]) if pd.notna(row["Runtime"]) else None
        },
        "Overview": {
            "rich_text": [
                {
                    "text": {
                        "content": (
                            str(row["Overview"])[:2000]
                            if pd.notna(row["Overview"])
                            else ""
                        )
                    }
                }
            ]
        },
        "VoteAverage": {
            "number": (
                float(row["VoteAverage"]) if pd.notna(row["VoteAverage"]) else None
            )
        },
        "VoteCount": {
            "number": int(row["VoteCount"]) if pd.notna(row["VoteCount"]) else None
        },
        "Popularity": {
            "number": float(row["Popularity"]) if pd.notna(row["Popularity"]) else None
        },
        "Genres": {
            "multi_select": (
                [
                    {"name": genre.strip()}
                    for genre in str(row["Genres"]).split(",")
                    if genre.strip()
                ]
                if pd.notna(row["Genres"])
                else []
            )
        },
        "ProductionCompanies": {
            "rich_text": [
                {
                    "text": {
                        "content": (
                            str(row["ProductionCompanies"])[:2000]
                            if pd.notna(row["ProductionCompanies"])
                            else ""
                        )
                    }
                }
            ]
        },
        "PosterPath": {
            "rich_text": [
                {
                    "text": {
                        "content": (
                            str(row["PosterPath"])[:2000]
                            if pd.notna(row["PosterPath"])
                            else ""
                        )
                    }
                }
            ]
        },
        "BackdropPath": {
            "rich_text": [
                {
                    "text": {
                        "content": (
                            str(row["BackdropPath"])[:2000]
                            if pd.notna(row["BackdropPath"])
                            else ""
                        )
                    }
                }
            ]
        },
        "BackdropImage": {
            "files": (
                [
                    {
                        "name": "Backdrop",
                        "type": "external",
                        "external": {
                            "url": f"https://image.tmdb.org/t/p/w500{row['BackdropPath']}"
                        },
                    }
                ]
                if pd.notna(row["BackdropPath"])
                else []
            )
        },
    }

    try:
        notion.pages.update(page_id=page_id, properties=properties)
    except APIResponseError as e:
        print(f"Error updating page {page_id}: {e}")
        print(f"Problematic row: {row}")


def upload_to_notion(csv_file="data/updated_watched_movies.csv"):
    df = pd.read_csv(csv_file)
    existing_movies = get_existing_movies()

    for _, row in df.iterrows():
        tmdb_id = row["TmdbId"]

        try:
            if tmdb_id in existing_movies:
                pass
            else:
                create_notion_page(row)
                print(f"Added new movie: {row['Title']}")
        except Exception as e:
            print(f"Error processing movie {row['Title']}: {e}")
            continue


if __name__ == "__main__":
    upload_to_notion()
