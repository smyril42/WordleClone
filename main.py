"""
A Clone of the viral game Wordle.
by Merlin Pritlove

Run: main()
Changable Variables:
- HARD_MODE: bool
- VALID_GUESSES_FP: str
- VALID_ANSWERS_FP: str
"""

# pylint: disable=[E1101, E1102, E0213, C0116]

from random import choice
from typing import Optional
import pygame as pg

__all__ = []

# init
pg.init()

# # # GAME VARIABLES # # #
HARD_MODE: bool = False
VALID_GUESSES_FP: str = 'valid-guesses'
VALID_ANSWERS_FP: str = 'valid-answers'
# # # GAME VARIABLES # # #


# # # KONSTANTS # #  #
WORD_LENGTH = 5
COUNT_GUESSES = 6

SCREEN_SIZE = 450, 800

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption('PLAY WORDLE | BY MERLIN')
FONT_BIG = pg.font.SysFont('DejaVuSansMono', 53)
FONT_SMALL = pg.font.SysFont('DejaVuSansMono', 26)
BOX_SIZE = FONT_BIG.size(' ')[1] - 2, FONT_BIG.size(' ')[1] - 2
# colors
class Color:
    BLACK = 0, 0, 0
    GREEN = 0, 255, 0
    YELLOW = 230, 230, 140
    GRAY = 105, 105, 105
    LIGHT_GRAY = 150, 150, 150
    DARK_GRAY = 50, 50, 50
    BLUE = 0, 0, 255
    RED = 255, 0, 0
    WHITE = 255, 255, 255
# match types, textbox stati, game_stati
NO_MATCH = INACTIVE = LOST = UNPUSHED = 0
HALF_MATCH = ACTIVE = NEXT = PUSHED = 1
FULL_MATCH = LOCKED = WON = 2
DEBUG = 5
# # # KONSTANTS # #  #


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
        self.guesses = 0
        self.used_letters = set()

        print(self.secret_word)

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
        out = [0] * WORD_LENGTH
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
        for letter in word:
            self.add_letter(letter)

        return out

    def add_letter(self, letter):
        self.used_letters.add(letter)

    def reset(self, hard_mode: Optional[bool] = None):
        self.hard_mode = self.hard_mode if hard_mode is None else hard_mode
        self.checked_words = self.outs = []
        self.guesses = 0
        self.used_letters = set()

    @staticmethod
    def color_from_match(code):
        colors = {NO_MATCH: Color.GRAY, HALF_MATCH: Color.YELLOW,
                  FULL_MATCH: Color.GREEN, DEBUG: Color.BLUE}
        return colors[code]


wordle_engine = WordleEngine(hard_mode=HARD_MODE)


class InputBox:
    """A group of WORD_LENGTH boxes able to be written with letters"""
    def __init__(self, pos: tuple, active: bool = False):
        self.pos = pos
        self.state = ACTIVE if active else INACTIVE
        self.text = ''
        self.colors = []

    def _is_active(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs) if self.state == ACTIVE else None
        return inner

    @_is_active
    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if len(self.text) == WORD_LENGTH:
                    self.colors = wordle_engine.check(self.text)
                    if not self.colors:
                        return None

                    self.lock()
                    return WON if min(self.colors) == FULL_MATCH else NEXT

            elif pg.K_a <= event.key <= pg.K_z and len(self.text) < WORD_LENGTH:
                self.text += event.unicode.lower()

            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
        return None

    def draw(self, surface):
        for i in range(WORD_LENGTH):
            letter_box = (self.pos[0] + i * FONT_BIG.size(' ')[1] + 1, self.pos[1] + 1), BOX_SIZE
            if self.state == LOCKED and i < len(self.text):
                pg.draw.rect(surface, WordleEngine.color_from_match(self.colors[i]), letter_box)
            else:
                pg.draw.rect(surface, Color.WHITE, letter_box, 2)

        for i, letter in enumerate(self.text):
            letter_shift = round(FONT_BIG.size(' ')[1] - FONT_BIG.size(' ')[0]) / 2
            pos_letter = self.pos[0] + i * FONT_BIG.size(' ')[1] + 1 + letter_shift, self.pos[1] + 1
            surface.blit(FONT_BIG.render(letter.upper(), True, Color.WHITE), pos_letter)

    def deactivate(self):
        self.state = INACTIVE

    def activate(self):
        self.state = ACTIVE

    def lock(self):
        self.state = LOCKED

    def reset(self):
        self.text = ''
        self.state = INACTIVE


class ClickableButton:
    """A button doing something when being clicked"""
    def __init__(
            self, pos: tuple[int, int], size: tuple[int, int],
            display_icon_path: str, call_onclick,
            holdable: bool = False):
        self.pos, self.size = pos, size
        self.diplay_icon = pg.image.load(display_icon_path)
        self.call_onclick = call_onclick
        self.holdable = holdable
        self.state = UNPUSHED

        self.colors = {
            'passive': Color.LIGHT_GRAY,
            'hover': Color.WHITE,
            'active': Color.DARK_GRAY
            }

        self.button_surface = pg.Surface(self.size)
        self.rect = pg.Rect(*self.pos, *self.size)

    def updater(self):
        pos_mouse = pg.mouse.get_pos()
        self.button_surface.fill(self.colors['passive'])
        if self.rect.collidepoint(pos_mouse):
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.colors['active'])
                if self.holdable:
                    self.call_onclick()
                elif self.state == UNPUSHED:
                    self.state = PUSHED
                    self.call_onclick()
            else:
                self.state = UNPUSHED
                self.button_surface.fill(self.colors['hover'])

        self.button_surface.blit(self.diplay_icon, (
            (self.rect.width - self.diplay_icon.get_rect().width) / 2,
            (self.rect.height - self.diplay_icon.get_rect().height) / 2))

        screen.blit(self.button_surface, self.rect)

    def unpush(self):
        self.state = UNPUSHED

    def push(self):
        self.state = PUSHED

    def lock(self):
        self.state = LOCKED


def main():
    """Function containing the main level code"""
    def win():
        for box in text_boxes:
            box.lock()

    def loose():
        text_boxes[-1].lock()

    def reset_all():
        for i in text_boxes:
            i.reset()
        text_boxes[0].activate()

        wordle_engine.reset()

    game_active = True
    clock = pg.time.Clock()

    spacing = round(BOX_SIZE[0] / 2)

    text_boxes = [InputBox((BOX_SIZE[0], (i + 1) * BOX_SIZE[0] + i * spacing), not i) for i in range(6)]

    reset_button = ClickableButton((0, 0), (45, 45), 'reset_icon.png', reset_all)

    while game_active:
        print(wordle_engine.used_letters)
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
        screen.fill(Color.BLACK)
        for box in text_boxes:
            box.draw(screen)
        reset_button.updater()

        pg.display.update()
        clock.tick(10)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pg.quit()
        raise e
