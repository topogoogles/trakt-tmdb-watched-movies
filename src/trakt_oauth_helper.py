import requests
import webbrowser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Trakt.tv API configuration
TRAKT_CLIENT_ID = os.getenv("TRAKT_CLIENT_ID")
TRAKT_CLIENT_SECRET = os.getenv("TRAKT_CLIENT_SECRET")
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

# Step 1: Authorization
auth_url = f"https://trakt.tv/oauth/authorize?response_type=code&client_id={TRAKT_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
print(f"Please visit this URL to authorize the application: {auth_url}")
webbrowser.open(auth_url)

# Step 2: Get the authorization code
auth_code = input("Enter the authorization code: ")

# Step 3: Exchange the code for an access token
token_url = "https://api.trakt.tv/oauth/token"
data = {
    "code": auth_code,
    "client_id": TRAKT_CLIENT_ID,
    "client_secret": TRAKT_CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}

response = requests.post(token_url, json=data)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
    print("Please add these to your .env file")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
