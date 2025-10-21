# 🎵 Spotify → YouTube Music Migration

A Python project that migrates your **Spotify playlists** into **YouTube Music**,  
using the **Spotify Web API** and the **ytmusicapi** (Browser Auth).

No third-party transfer apps — just clean, transparent Python code.

---

## 🚀 Features

- Migrate **all** your playlists (or test with one)
- Works with **Browser Auth** for YouTube Music — no Google Cloud setup needed
- Reads private & collaborative Spotify playlists
- Matches songs by **ISRC**, then falls back to **title + artist**
- Supports **dry-run simulation** (see what would happen, no uploads)
- Logs and unmatched tracks saved for review
- Clean, modular structure — great for portfolio or DevOps demos

---

## 🧩 Project structure

```
spotify-to-ytmusic/
├─ src/
│  ├─ auth_spotify.py        # Spotify authentication
│  ├─ spotify_client.py      # Spotify API helpers
│  ├─ ytmusic_client.py      # YouTube Music API helpers
│  ├─ matcher.py             # Optional fuzzy matching
│  ├─ migrate.py             # Full migration logic
│  ├─ smoke_copy.py          # 3-track test
│  └─ utils.py               # Logging helpers
├─ docs/
│  └─ browser.json           # Created via browser auth (do NOT commit)
├─ data/
│  ├─ unmatched.json         # Unmatched songs
│  └─ logs/migrate.log       # Migration logs
├─ .env                      # Spotify credentials (local only)
├─ Makefile                  # Helper commands
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Setup

### 1️⃣ Clone and open the project

```bash
git clone https://github.com/<yourusername>/spotify-to-ytmusic.git
cd spotify-to-ytmusic
code .
```

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🔑 Configure Spotify credentials

Create a `.env` file in the project root with your Spotify Developer App credentials:

```bash
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

#### 🔍 Where to get these
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Click **Create App**
3. Choose **Web API** under capabilities
4. Set Redirect URI → `http://localhost:8888/callback`
5. Copy your **Client ID** and **Client Secret**
6. Paste them into `.env`

> The `.env` file is ignored by Git (`.gitignore`), so it stays private.

---

## 🔐 Authenticate APIs

### 🎧 Spotify authentication

```bash
make auth-spotify
```
This opens a browser window to log into Spotify and approve access.  
Once approved, a `.cache` file is created locally to store your token.

If successful, you’ll see your Spotify username printed in the terminal.

---

### 🎵 YouTube Music authentication (Browser Auth)

You don’t need Google Cloud or OAuth — we’ll use **browser auth** from `ytmusicapi`.

Run this command:

```bash
make auth-yt
```

This launches an interactive flow:

1. You’ll see a short instruction like:
   ```
   Copy your YouTube Music request headers into docs/browser.json
   ```
2. A browser tab will open for [YouTube Music](https://music.youtube.com).
3. Open **Developer Tools** → **Network tab** (F12).
4. Refresh the page, click any request (e.g., `browse?` or `player?`).
5. In the **Headers** tab, copy all **Request Headers** (Ctrl+A → Ctrl+C).
6. Paste them into the terminal when prompted (or directly into `docs/browser.json`).
7. Press **Enter**.

Once completed, you’ll have:
```
docs/browser.json
```

This file stores your session headers and allows authenticated access to your YouTube Music account.

> ⚠️ Keep this file private — it’s equivalent to a login token.

If it ever expires or stops working, just run:
```bash
make auth-yt
```
again to regenerate it.

---

## ▶️ Run the migration

### 🧪 Smoke test (3 tracks from 1 playlist)

Run a small test to confirm everything works:
```bash
make smoke
```

This will:
- Pick your first Spotify playlist
- Copy the first 3 tracks
- Create a temporary private playlist on YouTube Music

---

### 🧍 Dry-run (simulation, no changes)

```bash
make dry-run
```

This mode:
- Scans all your Spotify playlists
- Finds matches on YouTube Music
- **Does not** create or modify any playlists

It’s ideal for testing mappings and verifying results before doing the full import.

---

### 🏃 Full migration

Once you’re satisfied:
```bash
make migrate
```

This will:
- Create playlists on YouTube Music
- Match and add tracks
- Log all operations to `data/logs/migrate.log`

---

## 📁 Outputs

| File | Description |
|------|--------------|
| `data/logs/migrate.log` | Full migration log |
| `data/unmatched.json` | Tracks that could not be matched on YouTube Music |

---

## 🧹 Maintenance

```bash
make fmt      # Auto-format code (ruff + black)
make clean    # Remove logs, caches, .venv, unmatched.json
make logs     # Tail the live migration log
```

---

## 🧠 Tips

- Use `DRY_RUN=true make migrate` for safe simulation.
- Re-run `make auth-yt` anytime if YouTube cookies expire.
- You can open the logs live in VS Code’s terminal using:
  ```bash
  make logs
  ```
- Always keep `.env`, `.cache`, and `docs/browser.json` out of Git — they’re private credentials.

---

## 🏁 Roadmap ideas

- Incremental sync (detect new or removed tracks)
- CLI options: `--only-playlist`, `--public`
- Unit tests for fuzzy matcher
- Optional OAuth mode for YouTube Music (for CI/CD)
- Dockerfile for quick runs

---

**Made with ☕, 🎧, and Python by <Your Name>**