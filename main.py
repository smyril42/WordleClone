# Wordle Clone by Merlin Pritlove


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
        with open(VALID_ANSWERS_FP) as f:
            self.valid_answers = f.read().split()

        self.secret_word = choice(self.valid_answers) if word is None else word
        if self.secret_word not in self.valid_answers:
            raise ValueError(f'Invalid word: \'{word}\'')

        with open(VALID_GUESSES_FP) as f:
            self.valid_guesses = f.read().split()

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
            elif letter in self.secret_word and word[:i].count(letter) < self.secret_word.count(letter):
                out[i] = HALF_MATCH

        self.checked_words.append(word)
        self.guesses += 1

        self.outs.append(out)

        return out

    def reset(self, word: Optional[str] = None, hard_mode: Optional[bool] = None):
        self.hard_mode = self.hard_mode if hard_mode is None else hard_mode
        self.checked_words = self.outs = []
        self.guesses = 0

    @staticmethod
    def color_from_code(x):
        return BLUE if x == DEBUG else GRAY if x == NO_MATCH else YELLOW if x == HALF_MATCH else GREEN


wordle_engine = WordleEngine(hard_mode=HARD_MODE)


class InputBox:
    def __init__(self, pos: tuple, active: bool = False):
        self.pos = pos
        self.state = ACTIVE if active else INACTIVE
        self.rect = pg.Rect(self.pos[0] + 1, self.pos[1] + 1, FONT.size('H')[1] - 2, FONT.size('H')[1] - 2)
        self.current_color = WHITE
        self.text = ''
        self.colors = []

    def is_unlocked(func):
        def inner(self, *args, **kwargs):
            if self.state != 2:
                return func(self, *args, **kwargs)
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
        # pg.draw.rect(surface, self.current_color, self.rect, 2)
        for i in range(WORD_LENGHT):
            if self.state == LOCKED:
                rect_letter = [(self.rect.x + i * FONT.size(' ')[1] + 1, self.rect.y + 1), (FONT.size(' ')[1] - 2, FONT.size(' ')[1] - 2)]
                if i < len(self.text):
                    pg.draw.rect(surface, WordleEngine.color_from_code(self.colors[i]), rect_letter)
            else:
                rect_letter = [(self.rect.x + i * FONT.size(' ')[1] + 1, self.rect.y + 1), (FONT.size(' ')[1] - 2, FONT.size(' ')[1] - 2)]
                pg.draw.rect(surface, WHITE, rect_letter, 2)

        for i, letter in enumerate(self.text):
            surface.blit(FONT.render(letter.upper(), True, WHITE), (self.rect.x + i * FONT.size(' ')[1] + 1 + (FONT.size(' ')[1] - FONT.size(' ')[0]) / 2, self.rect.y + 1))

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

    spacing = 10

    text_boxes = [InputBox((BOX_SIZE, (i + 1) * BOX_SIZE + i * spacing), True if i == 0 else False) for i in range(6)]

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
