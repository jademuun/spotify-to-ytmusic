# -----------------------------
# Spotify → YouTube Music Migrator
# -----------------------------
# Run with: make <target>
# -----------------------------

.PHONY: venv install auth-spotify auth-yt smoke migrate dry-run fmt clean logs help

# ------------- Setup -------------

venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

# ------------- Auth -------------

auth-spotify:
	. .venv/bin/activate && python -c "from src.auth_spotify import get_spotify; print(get_spotify().current_user()['display_name'])"

auth-yt:
	. .venv/bin/activate && ytmusicapi browser --file docs/browser.json

# ------------- Run -------------

smoke:
	. .venv/bin/activate && python src/smoke_copy.py

migrate:
	. .venv/bin/activate && python src/migrate.py

dry-run:
	DRY_RUN=true . .venv/bin/activate && python src/migrate.py

# ------------- Dev tools -------------

fmt:
	. .venv/bin/activate && python -m pip install -U ruff black && ruff check --fix . && black .

logs:
	tail -f data/logs/migrate.log

# ------------- Cleanup -------------

clean:
	rm -rf .venv .cache data/unmatched.json data/logs/* __pycache__ */__pycache__
	echo "✅ Cleaned environment, caches, and logs"

# ------------- Help -------------

help:
	@echo ""
	@echo "🎵 Spotify → YouTube Music Migration Commands"
	@echo "---------------------------------------------"
	@echo "make install      – create venv + install dependencies"
	@echo "make auth-spotify – authenticate Spotify"
	@echo "make auth-yt      – authenticate YouTube Music (browser auth)"
	@echo "make smoke        – run short 3-track migration test"
	@echo "make migrate      – run full migration"
	@echo "make dry-run      – simulate migration (no playlist creation)"
	@echo "make fmt          – auto-format code (ruff + black)"
	@echo "make logs         – tail live migration log"
	@echo "make clean        – delete logs, cache, and venv"
	@echo ""
