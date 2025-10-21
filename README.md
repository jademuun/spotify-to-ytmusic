# Spotify → YouTube Music Migration

A personal Python project to migrate your Spotify playlists into YouTube Music using the Spotify Web API and `ytmusicapi` (browser auth).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Authenticate

Spotify (creates .cache):
```bash
make auth-spotify
```

YouTube Music (browser auth → docs/browser.json):
```bash
make auth-yt
```

## Run Migration
Dry-run (no changes):
```bash
DRY_RUN=true make migrate
```

Full run:
```bash
make migrate
```

Logs → `data/logs/migrate.log`
Unmatched → `data/unmatched.json`
