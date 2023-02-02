import pygame as pg
from Colors import Color

pg.init()

NO_MATCH = INACTIVE = LOST = 0
HALF_MATCH = ACTIVE = NEXT = 1
FULL_MATCH = LOCKED = WON = 2

WORD_LENGTH = 5

FONT_SIZE_BIG = 53
FONT_BIG = pg.font.SysFont('DejaVuSansMono', FONT_SIZE_BIG)

BOX_SIZE = FONT_BIG.size(' ')[1] - 2, FONT_BIG.size(' ')[1] - 2


class InputBox:
    """A group of WORD_LENGTH boxes able to be written with letters"""
    def __init__(self, pos, game_engine, active=False):
        self.pos = pos
        self.game_engine = game_engine
        self.state = ACTIVE if active else INACTIVE
        self.text = ''
        self.match = []

    @staticmethod
    def _is_active(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs) if self.state == ACTIVE else None
        return inner

    @_is_active
    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if len(self.text) == WORD_LENGTH:
                    self.match = self.game_engine.check(self.text)
                    if not self.match:
                        return None

                    self.lock()
                    return WON if min(self.match) == FULL_MATCH else NEXT

            elif pg.K_a <= event.key <= pg.K_z and len(self.text) < WORD_LENGTH:
                self.text += event.unicode.lower()

            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
        return None

    def draw(self, surface):
        for i in range(WORD_LENGTH):
            letter_box = (self.pos[0] + i * FONT_BIG.size(' ')[1] + 1, self.pos[1] + 1), BOX_SIZE
            if self.state == LOCKED and i < len(self.text):
                pg.draw.rect(surface, self.game_engine.color_from_match(self.match[i]), letter_box)
            else:
                pg.draw.rect(surface, Color.INPUT_BOX, letter_box, 2)

        for i, letter in enumerate(self.text):
            letter_shift = round(FONT_BIG.size(' ')[1] - FONT_BIG.size(' ')[0]) / 2
            pos_letter = self.pos[0] + i * FONT_BIG.size(' ')[1] + 1 + letter_shift, self.pos[1] + 1
            surface.blit(FONT_BIG.render(letter.upper(), True, Color.INPUT_LETTER), pos_letter)

    def deactivate(self):
        self.state = INACTIVE

    def activate(self):
        self.state = ACTIVE

    def lock(self):
        self.state = LOCKED

    def reset(self):
        self.text = ''
        self.state = INACTIVE
