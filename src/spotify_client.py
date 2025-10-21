from typing import Iterator, Dict, List
from spotipy import Spotify
from itertools import islice

def iter_playlists(sp: Spotify) -> Iterator[Dict]:
    page = sp.current_user_playlists(limit=50)
    while True:
        for p in page["items"]:
            yield p
        if page["next"]:
            page = sp.next(page)
        else:
            break

def iter_playlist_tracks(sp: Spotify, playlist_id: str) -> Iterator[Dict]:
    page = sp.playlist_items(playlist_id, additional_types=("track",), limit=100)
    while True:
        for it in page["items"]:
            tr = it.get("track")
            if tr: yield tr
        if page["next"]:
            page = sp.next(page)
        else:
            break

def chunked(items, chunk_size):
    it = iter(items)
    while True:
        batch = list(islice(it, chunk_size))
        if not batch: break
        yield batch

def hydrate_isrcs(sp: Spotify, track_ids: List[str]) -> Dict[str, str]:
    out = {}
    for batch in chunked(track_ids, 50):
        res = sp.tracks(batch)["tracks"]
        for t in res:
            if t and t.get("external_ids", {}).get("isrc"):
                out[t["id"]] = t["external_ids"]["isrc"]
    return out
