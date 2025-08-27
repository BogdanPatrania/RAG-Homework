# src/utils/moderation.py
from __future__ import annotations

from pathlib import Path
from typing import List
from better_profanity import profanity
import urllib.request
import urllib.error

# Where we keep the Romanian bad-words list in the repo
_WORDLIST_DIR = Path("data/external")
_WORDLIST_FILE = _WORDLIST_DIR / "badwords_ro.txt"

# Source for Romanian list (what you'd do with curl)
_BADWORDS_URL = "https://raw.githubusercontent.com/Mihaidev-cloud/swear-words-romanian/master/ro"

# Minimal built-in fallback so the app doesn't break if download fails
_FALLBACK_RO_WORDS: List[str] = [
    "pula",
    "pizda",
    "dracu",
    "bou",
    "proasta",
    "prost",
    "idiot",
    "idiota",
    "bulangiu",
]

_loaded = False


def _download_wordlist_if_missing() -> None:
    """
    Ensure data/external/badwords_ro.txt exists.
    If it's missing, create the directory and download it from GitHub.
    This mirrors:
        mkdir -p data/external
        curl -L "<URL>" -o data/external/badwords_ro.txt
    """
    _WORDLIST_DIR.mkdir(parents=True, exist_ok=True)

    if _WORDLIST_FILE.exists() and _WORDLIST_FILE.stat().st_size > 0:
        return

    try:
        with urllib.request.urlopen(_BADWORDS_URL, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
        # Basic sanity check: ensure we got some lines
        lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        if len(lines) < 5:
            # Too few lines? Treat as failure and use fallback
            raise ValueError("Downloaded list seems too short")
        _WORDLIST_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        # Write fallback to keep the app functional
        _WORDLIST_FILE.write_text("\n".join(_FALLBACK_RO_WORDS) + "\n", encoding="utf-8")


def _ensure_loaded() -> None:
    """
    Lazy init:
      1) Make sure the wordlist file exists (download if needed)
      2) Load it into better_profanity
    """
    global _loaded
    if _loaded:
        return

    _download_wordlist_if_missing()

    words = []
    if _WORDLIST_FILE.exists():
        words = [
            w.strip()
            for w in _WORDLIST_FILE.read_text(encoding="utf-8").splitlines()
            if w.strip()
        ]

    # Initialize better_profanity with our Romanian list.
    # Note: You could merge with the default EN list by calling
    # profanity.load_censor_words() first, then profanity.add_censor_words(words).
    profanity.load_censor_words(words)
    _loaded = True


def is_inappropriate(text: str) -> bool:
    """
    Return True if the text contains profanity (Romanian list).
    """
    _ensure_loaded()
    return profanity.contains_profanity(text or "")


def censor(text: str) -> str:
    """
    Return a censored version of the text using '*'.
    """
    _ensure_loaded()
    return profanity.censor(text or "", censor_char="*")


def reload_wordlist(force_download: bool = False) -> None:
    """
    Utility to refresh the list at runtime, e.g., from an admin action.
    If force_download=True, re-fetch from GitHub even if the file exists.
    """
    global _loaded
    if force_download:
        try:
            # Try to download a fresh copy
            with urllib.request.urlopen(_BADWORDS_URL, timeout=10) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
            lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
            if len(lines) >= 5:
                _WORDLIST_DIR.mkdir(parents=True, exist_ok=True)
                _WORDLIST_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except Exception:
            # If refresh fails, keep the existing file as-is
            pass

    _loaded = False
    _ensure_loaded()
