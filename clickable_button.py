import pygame as pg
from Colors import Color


UNPUSHED = 0
PUSHED = 1
LOCKED = 2


class ClickableButton:
    """A button doing something when being clicked"""
    def __init__(
            self, pos, size, surface,
            display_icon_path, call_onclick):
        self.pos, self.size = pos, size
        self.surface = surface
        self.diplay_icon = pg.image.load(display_icon_path)
        self.call_onclick = call_onclick
        self.state = UNPUSHED

        self.button_surface = pg.Surface(self.size)
        self.rect = pg.Rect(*self.pos, *self.size)

    def updater(self):
        pos_mouse = pg.mouse.get_pos()
        self.button_surface.fill(Color.BUTTON_PASSIVE)
        if self.rect.collidepoint(pos_mouse):
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(Color.BUTTON_ACTIVE)
                if self.state == UNPUSHED:
                    self.push()
            else:
                self.unpush()
                self.button_surface.fill(Color.BUTTON_HOVER)

        self.button_surface.blit(self.diplay_icon, (
            (self.rect.width - self.diplay_icon.get_rect().width) / 2,
            (self.rect.height - self.diplay_icon.get_rect().height) / 2))

        self.surface.blit(self.button_surface, self.rect)

    def unpush(self):
        self.state = UNPUSHED

    def push(self):
        self.state = PUSHED
        self.call_onclick()

    def lock(self):
        self.state = LOCKED
