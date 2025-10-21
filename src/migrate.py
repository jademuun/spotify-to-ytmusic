import os, json, time, logging
from dotenv import load_dotenv
from tqdm import tqdm
from tenacity import retry, wait_exponential, stop_after_attempt
from auth_spotify import get_spotify
from spotify_client import iter_playlists, iter_playlist_tracks, hydrate_isrcs
from ytmusic_client import get_yt, ensure_playlist, search_song_video_id, add_items
from utils import setup_logging

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

# Delay between playlist migrations to avoid hitting API rate limits
RATE_LIMIT_DELAY = 0.2

@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(5))
def safe_add_items(yt, playlist_id, vids):
    add_items(yt, playlist_id, vids)

def main():
    load_dotenv()
    setup_logging()
    sp = get_spotify()
    yt = get_yt()
    logging.info("Starting migration (dry_run=%s)", DRY_RUN)

    unmatched = []
    for p in iter_playlists(sp):
        title = p["name"]
        desc  = f"Imported from Spotify ({p['id']})"
        logging.info("→ Migrating playlist: %s", title)

        pl_id = ensure_playlist(yt, title, desc, "PRIVATE") if not DRY_RUN else None

        tracks = list(iter_playlist_tracks(sp, p["id"]))
        sp_ids = [t["id"] for t in tracks if t and t.get("id")]
        isrcs = hydrate_isrcs(sp, sp_ids)

        video_ids = []
        for t in tqdm(tracks, unit="track"):
            if not t or not t.get("name"):
                continue
            artists = [a["name"] for a in (t.get("artists") or [])]
            vid = search_song_video_id(yt, isrc=isrcs.get(t.get("id")), title=t["name"], artists=artists)
            if vid:
                video_ids.append(vid)
            else:
                unmatched.append({
                    "playlist": title,
                    "spotify_track": {
                        "id": t.get("id"),
                        "name": t.get("name"),
                        "artists": artists,
                        "isrc": isrcs.get(t.get("id"))
                    }
                })

        if DRY_RUN:
            logging.info("[dry-run] Would add %d items to '%s'", len(video_ids), title)
        elif video_ids:
            safe_add_items(yt, pl_id, video_ids)
            logging.info("Added %d items to '%s'", len(video_ids), title)
            time.sleep(0.2)
            time.sleep(RATE_LIMIT_DELAY)
    if unmatched:
        os.makedirs("data", exist_ok=True)
        with open("data/unmatched.json", "w", encoding="utf-8") as f:
            json.dump(unmatched, f, ensure_ascii=False, indent=2)
        logging.info("Unmatched saved to data/unmatched.json (%d tracks)", len(unmatched))

if __name__ == "__main__":
    main()
