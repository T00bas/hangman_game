"""
main.py
Functional Hangman with scoring, stats, and logging.
Allows multiple rounds until the user quits.
"""

from pathlib import Path
from game.wordlist import load_words, pick_random_word
from game.engine import (
    initialize_game, process_guess,
    get_progress, get_guessed_letters,
    remaining_attempts, is_won, is_lost,
    calculate_score, load_statistics, update_statistics,
    create_log_folder, write_game_log
)
from ui.display import (
    show_welcome, show_new_round, show_progress,
    show_guessed_letters, show_remaining_attempts,
    show_message, show_round_end
)


def play_round(words, stats):
    """Play a single Hangman round and update logs/statistics."""
    secret = pick_random_word(words)
    state = initialize_game(secret)
    folder = create_log_folder()

    show_new_round(len(secret))
    show_progress(get_progress(state))
    show_guessed_letters(get_guessed_letters(state))
    show_remaining_attempts(remaining_attempts(state))

    while True:
        user_input = input("Enter a letter(s) or full word ('quit' to exit): ").strip()
        if not user_input:
            show_message("Please enter something.")
            continue

        # Allow user to exit mid-round
        if user_input.lower() in ("quit", "exit"):
            show_message("Exiting the current round.")
            return stats, "quit"

        result = process_guess(state, user_input)
        show_message(result["message"])
        show_progress(get_progress(state))
        show_guessed_letters(get_guessed_letters(state))
        show_remaining_attempts(remaining_attempts(state))

        if result["result"] == "win" or is_won(state):
            score = calculate_score(state["word"], state["wrong_count"])
            stats = update_statistics(stats, True, score)
            show_round_end(True, state["word"], state["wrong_count"])
            show_message(f"Points earned: {score}")
            write_game_log(folder, state, True, score, stats)
            return stats, "win"

        elif result["result"] == "lose" or is_lost(state):
            stats = update_statistics(stats, False, 0)
            show_round_end(False, state["word"], state["wrong_count"])
            write_game_log(folder, state, False, 0, stats)
            return stats, "lose"


def main():
    """Main gameplay loop — keeps running new words until user quits."""
    show_welcome()
    words_path = Path(__file__).resolve().parents[0] / "words" / "words.txt"

    try:
        words = load_words(words_path)
    except Exception as e:
        print("Error loading words:", e)
        return

    stats = load_statistics()

    while True:
        stats, outcome = play_round(words, stats)
        if outcome == "quit":
            show_message("Thank you for playing Hangman! 🎮")
            break

        # Ask player if they want another round
        again = input("\nDo you want to play another word? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            show_message("Goodbye! 👋 Your progress has been saved.")
            break


if __name__ == "__main__":
    main()
