import logging, os, sys

def setup_logging():
    os.makedirs("data/logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler("data/logs/migrate.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
