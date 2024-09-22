# TRAKT TMDB Watched Movies

The project synchronizes watched movies data between Trakt.Tv and TheMovieDB.org fetching additional movie details and serving two updated CSV local files containing the databases with this information.

## Project Goals

1. Maintain a local record of watched movies.
2. Enhance the local database with detailed information from watched movies.
3. Provide a seamless experience for users to track their watched movies.

## Project Structure

```bash
project_root/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── trakt_oauth_helper.py    
│   └── trakt_scraper.py
│
├── data/
│   ├── sample_watched_movies.csv
│   └── sample_updated_watched_movies.csv
│
├── venv/
│
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

Copy the credentials from the output and edit the `.env` file with:

```text
TRAKT_ACCESS_TOKEN=your_access_token_here
TRAKT_REFRESH_TOKEN=your_refresh_token_here
```
Save the `.env` file again
 
5. __Run the Script__: Execute the main Python file:

```
python src/main.py
```

## How It Works

1. The script uses the `trakt_scraper` module connecting to the __Trakt.tv__ API to fetch the user's watched movies history. The app also processes the received data, extracting relevant information like **TraktId, ImdbId, TmdbId, title, year,** and **watch date**. It groups the data by movie, counting the number of plays and keeping the most recent watch date. It saves the results to a CSV file named `watched_movies.csv` in the `data/` directory
2. Then it reads the `watched_movies.csv` file and using the `TmdbId` it fetches additional details from TheMovieDB.org API and it returns an `updated_watched_movies.csv` file appending all the new data
3. Each python file in the `src/` directory can be run separately providing real-time information in the terminal about the gathered information.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for discussion.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
