"""
display.py
Handles user interface: printing messages, progress, and game updates.
"""

from typing import List


def show_welcome():
    print("\n===============================")
    print("   WELCOME TO HANGMAN GAME!")
    print("===============================\n")


def show_new_round(word_length: int):
    print(f"New word selected! (Length: {word_length})\n")


def show_progress(progress: str):
    print(f"Word: {progress}")


def show_guessed_letters(letters: List[str]):
    if not letters:
        print("Guessed letters: None")
    else:
        print("Guessed letters:", ", ".join(letters))


def show_remaining_attempts(attempts: int):
    print(f"Remaining attempts: {attempts}\n")


def show_message(message: str):
    print(message)


def show_round_end(win: bool, word: str, wrong_guesses: int):
    print("\n===============================")
    if win:
        print(f"🎉 You win! The word was: {word}")
    else:
        print(f"❌ You lose. The word was: {word}")
    print(f"Wrong guesses: {wrong_guesses}")
    print("===============================\n")
