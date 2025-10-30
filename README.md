Hangman game 
A terminal-based implemented in Python using a modular, function-based structure.

The game supports single-letter, multi-letter, and full-word guesses, scoring, persistent statistics, and per-game logging.

Wordlist Format (words/words.txt)

The file contains at least 1000 comma-separated words.

Scoring System score = (wordlength * 10) - (wrongguesses * 5) On win, adds score to total On loss, adds 0 points

There are Persistent Statistics using every game played ever.

There is a logging system with log.txt which is written in the folder created for each game, inside game_log folder.

Game Logic: The Hangman game begins by randomly selecting a secret word from the provided words.txt file. The player’s goal is
to correctly guess this word within a limited number of wrong attempts (default is 6). During each round, the player can guess
a single letter, multiple adjoining letters, or even the entire word at once. Correct guesses reveal their positions in the hidden
word, while incorrect guesses reduce the remaining attempts. The game continues until the player either reveals the full word (win) 
or exhausts all attempts (loss). After each round, the player’s performance is evaluated using a 
scoring formula — (word_length × 10) − (wrong_guesses × 5) — and their statistics (wins, losses, total score, win rate, and average score) are 
updated and stored persistently. Each game’s full history, including guesses, results, and cumulative stats, is recorded in a uniquely numbered 
folder under game_log/. The player can continue playing multiple rounds or exit at any time by typing quit.