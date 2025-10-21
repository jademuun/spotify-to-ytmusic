from typing import List, Optional
from ytmusicapi import YTMusic

def get_yt():
    try:
        return YTMusic("docs/browser.json")
    except FileNotFoundError:
        print("Error: 'docs/browser.json' not found. Please run authentication first (see https://ytmusicapi.readthedocs.io/en/latest/setup.html).")
        raise

def ensure_playlist(yt: YTMusic, title: str, description: str="", privacy="PRIVATE") -> str:
    for pl in yt.get_library_playlists(limit=1000):
        if pl.get("title") == title:
            return pl["playlistId"]
    return yt.create_playlist(title, description, privacy)

def search_song_video_id(yt: YTMusic, *, isrc: Optional[str], title: str, artists: List[str]) -> Optional[str]:
    if isrc:
        res = yt.search(isrc, filter="songs")
        if res:
            vid = res[0].get("videoId")
            if vid: return vid
    q = f"{title} {artists[0] if artists else ''}".strip()
    res = yt.search(q, filter="songs")
    if res and res[0].get("videoId"):
        return res[0]["videoId"]
    res = yt.search(q, filter="videos")
    if res and res[0].get("videoId"):
        return res[0]["videoId"]
    return None

def add_items(yt: YTMusic, playlist_id: str, video_ids: List[str]):
    for i in range(0, len(video_ids), 100):
        yt.add_playlist_items(playlist_id, video_ids[i:i+100])
