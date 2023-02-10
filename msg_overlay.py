import pygame as pg
from constants import Constants as Const
from colors import Color


pg.init()


class MsgOverlay:
    def __init__(self, msg, surface, color=None):
        self.msg = msg
        self.surface = surface
        self.visible = False
        self.text_color = Color.MSG_TEXT if color is None else color
        self.box_color = Color.MSG_BOX
        self.msg_surface = Const.FONT_BIG.render(self.msg, True, self.text_color)
        self.pos = tuple((Const.SCREEN_SIZE[i] - self.msg_surface.get_size()[i]) / 2 for i in range(2))

        self.blackout = pg.Surface(Const.SCREEN_SIZE)
        self.blackout.set_alpha(200)
        self.blackout.fill(Color.MSG_BLACKOUT)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def set_msg(self, msg):
        self.msg = msg
        self.pos = tuple((Const.SCREEN_SIZE[i] - self.msg_surface.get_size()[i]) / 2 for i in range(2))
        self.msg_surface = Const.FONT_BIG.render(self.msg, True, self.text_color)

    def set_text_color(self, rgb):
        self.text_color = rgb
        self.msg_surface = Const.FONT_BIG.render(self.msg, True, self.text_color)

    @staticmethod
    def _is_visible(func):
        def inner(self, *args, **kwargs):
            if self.visible:
                return func(self, *args, **kwargs)
        return inner

    @staticmethod
    def _blackout(func):
        def inner(self, *args, **kwargs):
            self.surface.blit(self.blackout, (0, 0))
            return func(self, *args, **kwargs)
        return inner

    @_is_visible
    @_blackout
    def draw(self):
        pg.draw.rect(self.surface, self.box_color, (self.pos, self.msg_surface.get_size()))
        self.surface.blit(self.msg_surface, self.pos)
