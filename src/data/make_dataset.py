import os
from pathlib import Path

def ensure_dirs():
    for d in ["data/raw", "data/processed", "data/external"]:
        Path(d).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_dirs()
    print("Data directories ensured.")
