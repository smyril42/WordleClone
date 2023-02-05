import pygame as pg
from constants import Constants as Const
from colors import Color


pg.init()


class InputBox:
    """A group of WORD_LENGTH boxes able to be written with letters"""
    def __init__(self, pos, game_engine, active=False):
        self.pos = pos
        self.game_engine = game_engine
        self.state = Const.ACTIVE if active else Const.INACTIVE
        self.text = ''
        self.match = []

    @staticmethod
    def _is_active(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs) if self.state == Const.ACTIVE else None
        return inner

    @_is_active
    def event_handler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if len(self.text) == Const.WORD_LENGTH:
                    self.match = self.game_engine.check(self.text)
                    if not self.match:
                        return None

                    self.lock()
                    return Const.WON if min(self.match) == Const.FULL_MATCH else Const.NEXT

            elif pg.K_a <= event.key <= pg.K_z and len(self.text) < Const.WORD_LENGTH:
                self.text += event.unicode.lower()

            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
        return None

    def draw(self, surface):
        for i in range(Const.WORD_LENGTH):
            letter_box = (self.pos[0] + i * Const.FONT_BIG.size(' ')[1] + 1, self.pos[1] + 1), Const.BOX_SIZE
            if self.state == Const.LOCKED and i < len(self.text):
                pg.draw.rect(surface, self.game_engine.color_from_match(self.match[i]), letter_box)
            else:
                pg.draw.rect(surface, Color.INPUT_BOX, letter_box, 2)

        for i, letter in enumerate(self.text):
            letter_shift = round(Const.FONT_BIG.size(' ')[1] - Const.FONT_BIG.size(' ')[0]) / 2
            pos_letter = self.pos[0] + i * Const.FONT_BIG.size(' ')[1] + 1 + letter_shift, self.pos[1] + 1
            surface.blit(Const.FONT_BIG.render(letter.upper(), True, Color.INPUT_LETTER), pos_letter)

    def deactivate(self):
        self.state = Const.INACTIVE

    def activate(self):
        self.state = Const.ACTIVE

    def lock(self):
        self.state = Const.LOCKED

    def reset(self):
        self.text = ''
        self.state = Const.INACTIVE
