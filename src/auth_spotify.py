import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def get_spotify():
    # Load .env so this works even outside `make`
    load_dotenv()

    # Scopes you need for reading playlists; add more if required
    scope = "playlist-read-private playlist-read-collaborative"

    auth = SpotifyOAuth(
        scope=scope,
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        open_browser=False,          # <-- don’t try to xdg-open
        show_dialog=False            # set True if you want to force re-consent
    )
    return Spotify(auth_manager=auth)