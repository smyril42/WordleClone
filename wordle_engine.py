from typing import Optional
from random import choice
from Colors import GRAY, YELLOW, GREEN, BLUE

__all__ = ['WordleEngine']

VALID_GUESSES_FP: str = 'valid-guesses'
VALID_ANSWERS_FP: str = 'valid-answers'

WORD_LENGTH = 5

NO_MATCH = 0
HALF_MATCH = 1
FULL_MATCH = 2
DEBUG = 5

class WordleEngine:
    """Instances generate and hold the secret word and statistical data about the game."""
    def __init__(self, word: Optional[str] = None, hard_mode: bool = False) -> None:
        with open(VALID_ANSWERS_FP, 'r', encoding='utf-8') as file:
            self.valid_answers = file.read().split()

        self.secret_word = choice(self.valid_answers) if word is None else word
        if self.secret_word not in self.valid_answers:
            raise ValueError(f'Invalid word: \'{word}\'')

        with open(VALID_GUESSES_FP, 'r', encoding='utf-8') as file:
            self.valid_guesses = file.read().split()

        self.hard_mode = hard_mode
        self.checked_words = self.outs = []
        self.letters = {}
        self.guesses = 0

        print(self.secret_word)

    @staticmethod
    def _hard_check(func):
        def inner(self, word, *args, **kwargs):
            if (not self.hard_mode) or (not self.checked_words):
                return func(self, word, *args, **kwargs)

            for i, match_type in enumerate(self.outs[-1]):
                if match_type == FULL_MATCH and word[i] != self.checked_words[-1][i]:
                    return []
            return func(self, word, *args, **kwargs)
        return inner

    @_hard_check
    def check(self, word):
        matches = [0] * WORD_LENGTH
        if word not in self.valid_guesses:
            return []

        for i, letter in enumerate(word):
            if letter == self.secret_word[i]:
                matches[i] = FULL_MATCH
            elif letter in self.secret_word:
                if word[:i].count(letter) < self.secret_word.count(letter):
                    matches[i] = HALF_MATCH

        self.checked_words.append(word)
        self.guesses += 1

        for match_type, letter in zip(matches, word):
            if letter not in self.letters:
                self.letters[letter] = match_type

        return matches

    def reset(self, hard_mode: Optional[bool] = None):
        self.hard_mode = self.hard_mode if hard_mode is None else hard_mode
        self.checked_words = self.outs = []
        self.letters = {}
        self.guesses = 0

    @staticmethod
    def color_from_match(code):
        colors = {NO_MATCH: GRAY, HALF_MATCH: YELLOW,
                  FULL_MATCH: GREEN, DEBUG: BLUE}
        return colors[code]
