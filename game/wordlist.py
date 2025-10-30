"""
wordlist.py
Handles loading and validating the word list, ensuring random selection
and a minimum of 1000 valid words.
"""

from pathlib import Path
import random
from typing import List

WORDS_FILE = Path(__file__).resolve().parents[1] / "words" / "words.txt"


def load_words(path: Path = None) -> List[str]:
    """Load words from a comma-separated file ending with a period."""
    p = path or WORDS_FILE
    if not p.exists():
        raise FileNotFoundError(f"Wordlist not found at {p}")

    with p.open("r", encoding="utf-8") as f:
        text = f.read().strip()

    if text.endswith("."):
        text = text[:-1]

    # Split by commas, clean spaces, lowercase
    words = [w.strip().lower() for w in text.split(",") if w.strip()]

    # Validate at least 1000 words
    if len(words) < 1000:
        raise ValueError(f"Word list must contain at least 1000 words (found {len(words)}).")

    return words


def pick_random_word(words: List[str]) -> str:
    """Pick and return a random word from the list."""
    return random.choice(words)
