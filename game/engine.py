"""
engine.py
Handles Hangman gameplay logic, scoring, statistics, and logging.
Functional implementation — no classes used.
"""

from datetime import datetime
from pathlib import Path
import json


# -----------------------------
# GAME INITIALIZATION
# -----------------------------
def initialize_game(word: str, max_wrong: int = 6) -> dict:
    word = word.lower()
    return {
        "word": word,
        "max_wrong": max_wrong,
        "wrong_count": 0,
        "revealed": [ch if not ch.isalpha() else "_" for ch in word],
        "guessed_letters": set(),
        "correct_letters": set(),
        "unique_letters": {c for c in word if c.isalpha()},
        "guess_history": [],
        "start_time": datetime.now(),
    }


# -----------------------------
# BASIC HELPERS
# -----------------------------
def get_progress(state): return " ".join(state["revealed"])
def get_guessed_letters(state): return sorted(state["guessed_letters"])
def remaining_attempts(state): return state["max_wrong"] - state["wrong_count"]
def is_won(state): return state["correct_letters"] == state["unique_letters"]
def is_lost(state): return state["wrong_count"] >= state["max_wrong"]


# -----------------------------
# LETTER REVEALING
# -----------------------------
def reveal_letter(state, letter):
    count = 0
    for i, ch in enumerate(state["word"]):
        if ch == letter and state["revealed"][i] == "_":
            state["revealed"][i] = letter
            count += 1
    if count > 0:
        state["correct_letters"].add(letter)
    return count


# -----------------------------
# PROCESS GUESS INPUT
# -----------------------------
def process_guess(state, user_input):
    """Handle single letters, multi-letters, or full-word guesses."""
    s = user_input.strip().lower()
    if not s:
        return {"message": "Empty input. Try again.", "result": "continue"}

    # FULL-WORD GUESS (correct)
    if len(s) > 1 and s == state["word"]:
        for i, ch in enumerate(state["word"]):
            if ch.isalpha():
                state["revealed"][i] = ch
        state["correct_letters"] = state["unique_letters"].copy()
        state["guess_history"].append((s, "Correct (full word)"))
        return {"message": "🎯 Correct! Full word guessed!", "result": "win"}

    # FULL-WORD GUESS (wrong)
    if len(s) > 1 and s != state["word"] and s.isalpha():
        state["wrong_count"] += 1
        state["guess_history"].append((s, "Wrong (full word)"))
        return {
            "message": "❌ Wrong full-word guess!",
            "result": "lose" if is_lost(state) else "continue",
        }

    # MULTIPLE LETTERS (adjoining)
    if len(s) > 1 and s.isalpha():
        wrong_added = 0
        for letter in s:
            if letter not in state["guessed_letters"]:
                state["guessed_letters"].add(letter)
                revealed_now = reveal_letter(state, letter)
                if revealed_now == 0:
                    state["wrong_count"] += 1
                    wrong_added += 1
        msg = f"Processed sequence '{s}'. {wrong_added} wrong guesses added."
        if is_won(state):
            return {"message": msg + " You win!", "result": "win"}
        if is_lost(state):
            return {"message": msg + " You lose!", "result": "lose"}
        return {"message": msg, "result": "continue"}

    # SINGLE LETTER GUESS
    if len(s) == 1 and s.isalpha():
        letter = s
        if letter in state["guessed_letters"]:
            state["guess_history"].append((letter, "Repeated"))
            return {"message": f"'{letter}' already guessed.", "result": "continue"}

        state["guessed_letters"].add(letter)
        revealed_now = reveal_letter(state, letter)
        if revealed_now > 0:
            state["guess_history"].append((letter, "Correct"))
            msg = f"Correct! '{letter}' revealed."
            if is_won(state):
                return {"message": msg + " You win!", "result": "win"}
            return {"message": msg, "result": "continue"}
        else:
            state["wrong_count"] += 1
            state["guess_history"].append((letter, "Wrong"))
            msg = f"Wrong! '{letter}' not in word."
            if is_lost(state):
                return {"message": msg + " You lose!", "result": "lose"}
            return {"message": msg, "result": "continue"}

    # INVALID INPUT
    return {"message": "Invalid input. Use letters or full words only.", "result": "continue"}


# -----------------------------
# SCORING SYSTEM
# -----------------------------
def calculate_score(word: str, wrong_guesses: int) -> int:
    """Scoring formula: (word_length * 10) - (wrong_guesses * 5)"""
    score = (len(word) * 10) - (wrong_guesses * 5)
    return max(score, 0)


# -----------------------------
# STATISTICS MANAGEMENT
# -----------------------------
def get_stats_file():
    return Path(__file__).resolve().parents[1] / "game_log" / "stats.json"


def load_statistics():
    """Load persistent player statistics."""
    path = get_stats_file()
    if not path.exists():
        return {
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "total_score": 0,
            "win_rate": 0.0,
            "average_score": 0.0,
        }
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_statistics(stats: dict):
    """Save player statistics to file."""
    path = get_stats_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)


def update_statistics(stats: dict, win: bool, round_score: int):
    """Update stats after each game."""
    stats["games_played"] += 1
    if win:
        stats["wins"] += 1
    else:
        stats["losses"] += 1
    stats["total_score"] += round_score
    stats["win_rate"] = round((stats["wins"] / stats["games_played"]) * 100, 2)
    stats["average_score"] = round(stats["total_score"] / stats["games_played"], 2)
    save_statistics(stats)
    return stats


# -----------------------------
# GAME LOGGING
# -----------------------------
def create_log_folder():
    """Create a new folder (game1, game2, ...) for each game."""
    base = Path(__file__).resolve().parents[1] / "game_log"
    base.mkdir(parents=True, exist_ok=True)
    existing = [d for d in base.iterdir() if d.is_dir() and d.name.startswith("game")]
    folder = base / f"game{len(existing) + 1}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def write_game_log(folder, state, win, score, stats):
    """Write detailed log.txt file including game stats."""
    log_file = folder / "log.txt"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with log_file.open("w", encoding="utf-8") as f:
            # --- Header ---
            f.write("Game Log\n")
            f.write(f"Date & Time: {now}\n")
            f.write(f"Word: {state['word']}\n")
            f.write(f"Word Length: {len(state['word'])}\n")
            f.write(f"Result: {'Win' if win else 'Loss'}\n")
            f.write(f"Wrong Guesses: {state['wrong_count']}\n")
            f.write(f"Score: {score}\n\n")

            # --- Guess History ---
            f.write("--- Guesses (in order) ---\n")
            for i, (g, r) in enumerate(state["guess_history"], 1):
                f.write(f"{i}. {g} → {r}\n")

            wrong = [g for g, r in state["guess_history"] if "Wrong" in r]
            f.write(f"\nWrong Letters: {', '.join(wrong) if wrong else 'None'}\n")
            f.write(f"Remaining Attempts: {state['max_wrong'] - state['wrong_count']}\n")

            # --- Player Stats ---
            f.write("\n--- Cumulative Player Statistics ---\n")
            f.write(f"Games Played: {stats['games_played']}\n")
            f.write(f"Wins: {stats['wins']}\n")
            f.write(f"Losses: {stats['losses']}\n")
            f.write(f"Total Score: {stats['total_score']}\n")
            f.write(f"Win Rate: {stats['win_rate']}%\n")
            f.write(f"Average Score: {stats['average_score']}\n")

            f.write("\n---------------------------------------\n")

        # force file write to disk
        log_file.touch(exist_ok=True)
    except Exception as e:
        print("⚠️ Error writing game log:", e)