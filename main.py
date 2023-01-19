# Wordle Clone by Merlin Pritlove

# pylint: disable=[E1101, E1102, E0213]

# imports
from random import choice
from typing import Optional
import pygame as pg

__all__ = ['main']

# init
pg.init()

# # # GAME VARIABLES # # #
HARD_MODE: bool = True
VALID_GUESSES_FP = 'valid-guesses'
VALID_ANSWERS_FP = 'valid-answers'
# # # GAME VARIABLES # # #


# # # KONSTANTS # #  #
WORD_LENGHT = 5
COUNT_GUESSES = 6

screen = pg.display.set_mode((450, 800))
pg.display.set_caption('PLAY WORDLE | BY MERLIN')
FONT = pg.font.SysFont('DejaVuSansMono', 53)
BOX_SIZE = 45
LETTER_BOX_SIZE = FONT.size(' ')[1] - 2, FONT.size(' ')[1] - 2
# colors
BLACK = 0, 0, 0
GREEN = 0, 255, 0
YELLOW = 230, 230, 140
GRAY = 105, 105, 105
BLUE = 0, 0, 255
RED = 255, 0, 0
WHITE = 255, 255, 255
# match types, textbox stati, game_stati
NO_MATCH = INACTIVE = LOST = 0
HALF_MATCH = ACTIVE = NEXT = 1
FULL_MATCH = LOCKED = WON = 2
DEBUG = 5
# # # KONSTANTS # #  #

class WordleEngine:
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
        self.guesses = 0

        print(self.secret_word)

    def _hard_check(func):
        def inner(self, word, *args, **kwargs):
            if not self.checked_words:
                return func(self, word, *args, **kwargs)

            for i, match_type in enumerate(self.outs[-1]):
                if match_type == FULL_MATCH and word[i] != self.checked_words[-1][i]:
                    return []
            return func(self, word, *args, **kwargs)
        return inner

    @_hard_check
    def check(self, word):
        out = [0] * WORD_LENGHT
        if word not in self.valid_guesses:
            return []

        for i, letter in enumerate(word):
            if letter == self.secret_word[i]:
                out[i] = FULL_MATCH
            elif letter in self.secret_word:
                if word[:i].count(letter) < self.secret_word.count(letter):
                    out[i] = HALF_MATCH

        self.checked_words.append(word)
        self.guesses += 1

        self.outs.append(out)

        return out

    def reset(self, hard_mode: Optional[bool] = None):
        self.hard_mode = self.hard_mode if hard_mode is None else hard_mode
        self.checked_words = self.outs = []
        self.guesses = 0

    @staticmethod
    def color_from_code(code):
        colors = {NO_MATCH: GRAY, HALF_MATCH: YELLOW, FULL_MATCH: GREEN, DEBUG: BLUE}
        return colors[code]


wordle_engine = WordleEngine(hard_mode=HARD_MODE)


class InputBox:
    def __init__(self, pos: tuple, active: bool = False):
        self.pos = pos
        self.state = ACTIVE if active else INACTIVE
        self.current_color = WHITE
        self.text = ''
        self.colors = []

    def is_unlocked(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs) if self.state != 2 else None
        return inner

    @is_unlocked
    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if self.state == ACTIVE:
                if event.key == pg.K_RETURN:
                    if len(self.text) == WORD_LENGHT:
                        self.colors = wordle_engine.check(self.text)
                        if not self.colors:
                            return None

                        self.current_color = WHITE
                        self.lock()
                        return WON if min(self.colors) == FULL_MATCH else NEXT

                elif pg.K_a <= event.key <= pg.K_z and len(self.text) < WORD_LENGHT:
                    self.text += event.unicode.lower()

                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
        return None

    def draw(self, surface):
        for i in range(WORD_LENGHT):
            letter_box = (self.pos[0] + i * FONT.size(' ')[1] + 1, self.pos[1] + 1), LETTER_BOX_SIZE
            if self.state == LOCKED and i < len(self.text):
                pg.draw.rect(surface, WordleEngine.color_from_code(self.colors[i]), letter_box)
            else:
                pg.draw.rect(surface, WHITE, letter_box, 2)

        for i, letter in enumerate(self.text):
            letter_shift = round(FONT.size(' ')[1] - FONT.size(' ')[0]) / 2
            pos_letter = self.pos[0] + i * FONT.size(' ')[1] + 1 + letter_shift, self.pos[1] + 1
            surface.blit(FONT.render(letter.upper(), True, WHITE), pos_letter)

    def deactivate(self):
        self.state = INACTIVE

    def activate(self):
        self.state = ACTIVE

    def lock(self):
        self.state = LOCKED


def main():
    def win():
        for box in text_boxes:
            box.lock()

    def loose():
        text_boxes[-1].lock()

    game_active = True
    clock = pg.time.Clock()

    spacing = round(BOX_SIZE / 2)

    text_boxes = [InputBox((BOX_SIZE, (i + 1) * BOX_SIZE + i * spacing), not i) for i in range(6)]

    while game_active:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_active = False
                pg.quit()
                break

            for i, box in enumerate(text_boxes):
                out = box.event_handler(event)
                if out == WON:
                    win()
                elif out == NEXT:
                    if i + 1 != 6:
                        text_boxes[i + 1].activate()
                    else:
                        loose()

                elif out == LOST:
                    loose()

        # updating the screen
        screen.fill(BLACK)
        for box in text_boxes:
            box.draw(screen)

        pg.display.update()
        clock.tick(10)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pg.quit()
        raise e
