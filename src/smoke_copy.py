from auth_spotify import get_spotify
from spotify_client import iter_playlists, iter_playlist_tracks, hydrate_isrcs
from ytmusic_client import get_yt, ensure_playlist, search_song_video_id, add_items

sp = get_spotify()
yt = get_yt()

p = next(iter_playlists(sp))
print("Source:", p["name"])

tracks = []
for t in iter_playlist_tracks(sp, p["id"]):
    if t and t.get("id"):
        tracks.append(t)
    if len(tracks) >= 3:
        break

isrcs = hydrate_isrcs(sp, [t["id"] for t in tracks])
pl_id = ensure_playlist(yt, f"TEST: {p['name']}", "smoke copy", "PRIVATE")

vids = []
for t in tracks:
    artists = [a["name"] for a in (t.get("artists") or [])]
    vid = search_song_video_id(yt, isrc=isrcs.get(t["id"]), title=t["name"], artists=artists)
    if vid:
        vids.append(vid)

print("Resolved:", vids)
if vids:
    add_items(yt, pl_id, vids)
    print("Added", len(vids), "items to", pl_id)