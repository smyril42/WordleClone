from typing import Optional
from random import choice
from constants import Constants as Const
from colors import Color


with open(Const.VALID_ANSWERS_FP, 'r', encoding='utf-8') as file:
    valid_answers = file.read().split()

with open(Const.VALID_GUESSES_FP, 'r', encoding='utf-8') as file:
    valid_guesses = file.read().split()


class WordleEngine:
    """Instances generate and hold the secret word and statistical data about the game."""
    def __init__(self, word: Optional[str] = None, hard_mode: bool = False) -> None:
        self.secret_word = choice(valid_answers) if word is None else word
        if self.secret_word not in valid_answers:
            raise ValueError(f'Invalid word: \'{word}\'')

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
                if match_type == Const.FULL_MATCH and word[i] != self.checked_words[-1][i]:
                    return []
            return func(self, word, *args, **kwargs)
        return inner

    @_hard_check
    def check(self, word):
        matches = [0] * Const.WORD_LENGTH
        if word not in valid_guesses:
            return []

        for i, letter in enumerate(word):
            if letter == self.secret_word[i]:
                matches[i] = Const.FULL_MATCH
            elif letter in self.secret_word:
                if word[:i].count(letter) < self.secret_word.count(letter):
                    matches[i] = Const.HALF_MATCH

        self.checked_words.append(word)
        self.guesses += 1

        for match_type, letter in zip(matches, word):
            self.letters[letter] = match_type

        return matches

    def reset(self, hard_mode: Optional[bool] = None):
        self.hard_mode = self.hard_mode if hard_mode is None else hard_mode
        self.checked_words = self.outs = []
        self.letters = {}
        self.guesses = 0

    @staticmethod
    def color_from_match(code):
        colors = {Const.NO_MATCH: Color.NO_MATCH, Const.HALF_MATCH: Color.HALF_MATCH,
                  Const.FULL_MATCH: Color.FULL_MATCH, Const.DEBUG: Color.DEBUG}
        return colors[code]
