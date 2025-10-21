.PHONY: venv install auth-spotify auth-yt smoke migrate fmt

venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

auth-spotify:
	. .venv/bin/activate && python -c "from src.auth_spotify import get_spotify; print(get_spotify().current_user()['display_name'])"

auth-yt:
	. .venv/bin/activate && ytmusicapi browser --file docs/browser.json

smoke:
	. .venv/bin/activate && python src/smoke_copy.py

migrate:
	. .venv/bin/activate && python src/migrate.py

fmt:
	. .venv/bin/activate && python -m pip install ruff black && ruff check --fix . && black .
