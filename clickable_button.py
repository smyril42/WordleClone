import os
import pygame as pg
from constants import Constants as Const
from colors import Color

class ClickableButton:
    UNPUSHED = 0
    PUSHED = 1
    """A button doing something when being clicked"""
    def __init__(
            self, pos, size, surface,
            display_icon_path, call_onclick):
        self.pos, self.size = pos, size
        self.surface = surface
        self.display_icon = pg.image.load(str(os.path.dirname(__file__)) + '/' + str(display_icon_path))
        self.call_onclick = call_onclick
        self.state = self.UNPUSHED

        self.button_surface = pg.Surface(self.size)
        self.rect = pg.Rect(*self.pos, *self.size)

    def updater(self):
        pos_mouse = pg.mouse.get_pos()
        self.button_surface.fill(Color.BUTTON_PASSIVE)
        if self.rect.collidepoint(pos_mouse):
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(Color.BUTTON_ACTIVE)
                if self.state == self.UNPUSHED:
                    self.push()
            else:
                self.unpush()
                self.button_surface.fill(Color.BUTTON_HOVER)

        self.button_surface.blit(self.display_icon, (
            (self.rect.width - self.display_icon.get_rect().width) / 2,
            (self.rect.height - self.display_icon.get_rect().height) / 2))

        self.surface.blit(self.button_surface, self.rect)

    def unpush(self):
        self.state = self.UNPUSHED

    def push(self):
        self.state = self.PUSHED
        self.call_onclick()

    def lock(self):
        self.state = Const.ObjState.LOCKED
