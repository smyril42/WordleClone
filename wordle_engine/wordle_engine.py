import os.path
from typing import Optional
from random import choice
from constants import Constants as Const
from colors import Color


with open(f'{os.path.dirname(__file__)}/{Const.VALID_ANSWERS_FP}', 'r', encoding='utf-8') as file:
    valid_answers = file.read().split()

with open(f'{os.path.dirname(__file__)}/{Const.VALID_GUESSES_FP}', 'r', encoding='utf-8') as file:
    valid_guesses = file.read().split()


class WordleEngine:
    """Instances generate and hold the secret word and statistical data about the game."""
    def __init__(self, word: Optional[str] = None, *, hard_mode: bool = False) -> None:
        self.secret_word = self._new_secret_word(word=word)

        self.hard_mode = hard_mode
        self.checked_words = []
        self.outs = []
        self.letters = {}
        self.guesses = 0

        print(self.secret_word)

    @staticmethod
    def _new_secret_word(self, *, word: Optional[str] = None):
        if (out := choice(valid_answers) if word is None else word) in valid_answers:
            return out
        raise ValueError('Invalid word: \'' + word + '\'')

    @staticmethod
    def _hard_check(func):
        def inner(self, word, *args, **kwargs):
            if (not self.hard_mode) or (not self.checked_words):
                return func(self, word, *args, **kwargs)

            last_word = self.checked_words[-1]
            last_matches = self.outs[-1]
            last_word_no_greens = ''

            for i, letter, match_type in zip(range(Const.WORD_LENGTH), last_word, last_matches):
                if match_type != Const.FULL_MATCH:
                    last_word_no_greens += letter
                elif letter != word[i]:
                    return []

            for i, letter, match_type in zip(range(Const.WORD_LENGTH), last_word, last_matches):
                if match_type != Const.HALF_MATCH:
                    continue
                if last_word_no_greens.count(letter) > word.count(letter):
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
        self.outs.append(matches)
        self.guesses += 1

        for match_type, letter in zip(matches, word):
            self.letters[letter] = match_type

        return matches

    def reset(self, *, word: Optional[str] = None, hard_mode: Optional[bool] = None):
        self.secret_word = self._new_secret_word(word=word)
        self.hard_mode = self.hard_mode if hard_mode is None else hard_mode
        self.checked_words = []
        self.outs = []
        self.letters = {}
        self.guesses = 0

    @staticmethod
    def color_from_match(code):
        colors = {Const.NO_MATCH: Color.NO_MATCH, Const.HALF_MATCH: Color.HALF_MATCH,
                  Const.FULL_MATCH: Color.FULL_MATCH, Const.DEBUG: Color.DEBUG}
        return colors[code]
