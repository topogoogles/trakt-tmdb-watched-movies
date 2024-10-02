# TRAKT TMDB Watched Movies with Notion Integration

This project synchronizes watched movies data between Trakt.TV and TheMovieDB.org, fetching additional movie details and serving two updated CSV local files containing the databases with this information. It now also integrates with Notion, allowing you to upload the movie data to a Notion database.

## Project Goals

1. Maintain a local record of watched movies.
2. Enhance the local database with detailed information from watched movies.
3. Provide a seamless experience for users to track their watched movies.
4. Sync the watched movies data with a Notion database for easy access and visualization.

## Project Structure

```bash
project_root/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── trakt_oauth_helper.py
│   ├── trakt_scraper.py
│   └── notion_uploader.py
├── data/
│   ├── sample_watched_movies.csv
│   └── sample_updated_watched_movies.csv
├── venv/
├── .env
├── LICENSE
├── README.md
└── requirements.txt
```

## Setup Instructions

### Prerequisites

- Python 3.6+
- Virtual environment support
- Credentials for TheMovieDB.org and Trakt.tv APIs
- Notion API integration token and database ID

#### Getting the API Credentials

__TheMovieDB.org APP Registration:__

- Start by creating an account at <https://www.themoviedb.org>
- Go under Account> Settings> API
- Register your application filling the required fields
- Take note of the API key

__Trakt.tv Registration and OAuth Authorization:__

- First, make sure you have registered your application on Trakt.tv. Go to <https://trakt.tv/oauth/applications>
- Click on "New Application"
- Fill in the details (Name, Description, Redirect URI)
- For Redirect URI, you can use `urn:ietf:wg:oauth:2.0:oob` for a simple PIN-based flow
- Take note of the **Client ID** and **Client Secret** and continue with the Installation process for further instructions

__Notion API Integration:__

1. Go to https://www.notion.so/my-integrations and create a new integration.
2. Give it a name and select the workspace where your database is located.
3. After creation, you'll see an "Internal Integration Token". Copy this token.
4. In your Notion workspace, create a new database or use an existing one for your movies.
5. Share the database with your integration by clicking "Share" and inviting the integration.
6. Copy the database ID from the URL (it's the part after the workspace name and before the question mark).

### Installation

1. __Virtual Environment__: Create and activate a virtual environment

```
python -m venv venv
```
On Linux or macOS run
```
source venv/bin/activate
```
On Windows use type
```
venv\Scripts\activate
```

2. __Install Dependencies__: Install the required packages

```
pip install -r requirements.txt
```

3. __Set Up .env File__: Create a `.env` file in the root directory and add your credential keys by running the built-in Linux text editor

```
nano .env
```
Once inside the editor (or your IDE of choice editor) add the following:

```text
TMDB_API_KEY=your_themoviedb_api_key_here
TRAKT_CLIENT_SECRET=your_trakt_client_secret_here
TRAKT_CLIENT_ID=your_trakt_client_id_here
```
Replace `your_[credential]_here` with your actual credentials obtained in the previous steps above. Save the file and run 

```
trakt_oauth_helper.py
```
Copy the credentials from the output and update the `.env` file. Also make sure at this point to fill up the Notion credentials:

```text
NOTION_TOKEN=your_notion_integration_token_here
NOTION_DATABASE_ID=your_notion_database_id_here
```

4. __Run the Script__: Execute the main Python file:

```
python src/main.py
```

## How It Works

1. The script uses the trakt_scraper module connecting to the Trakt.tv API to fetch the user's watched movies history. The app also processes the received data, extracting relevant information like TraktId, ImdbId, TmdbId, title, year, and watch date. It groups the data by movie, counting the number of plays and keeping the most recent watch date. It saves the results to a CSV file named watched_movies.csv in the data/ directory

2. Then it reads the watched_movies.csv file and using the TmdbId it fetches additional details from TheMovieDB.org API and it returns an updated_watched_movies.csv file appending all the new data

3. After creating the `updated_watched_movies.csv` file, the script now uses the `notion_uploader` module to upload the movie data to the specified Notion database.

4. The `notion_uploader` module checks for existing entries in the Notion database to avoid duplicates. It updates existing entries and adds new ones as needed.

5. The Notion database is populated with detailed movie information, including a new "BackdropImage" property that links directly to the movie's backdrop image on TMDB.

6. Each Python file in the `src/` directory can be run separately, providing real-time information in the terminal about the gathered information and the Notion upload process.

## Notion Database Structure

The Notion database will include the following properties for each movie:

- Title
- Year
- WatchedAt
- Plays
- Tagline
- ReleaseDate
- Runtime
- Overview
- VoteAverage
- VoteCount
- Popularity
- Genres
- ProductionCompanies
- Slug
- TraktId
- ImdbId
- TmdbId
- PosterPath
- BackdropPath
- BackdropImage (file type property linking to the TMDB backdrop image)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for discussion.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
