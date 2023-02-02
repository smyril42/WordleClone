"""
A Clone of the viral game Wordle.
by Merlin Pritlove

Run: main()
"""

# pylint: disable=[E1101, E1102, E0213, C0116]

import pygame as pg
from wordle_engine import WordleEngine
from Colors import Color


# init
pg.init()

# # # GAME VARIABLES # # #
HARD_MODE: bool = False
# # # GAME VARIABLES # # #


# # # KONSTANTS # #  #
WORD_LENGTH = 5
COUNT_GUESSES = 6

SCREEN_SIZE = 450, 800
FONT_SIZE_BIG = 53
FONT_SIZE_SMALL = 26

screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption('PLAY WORDLE | BY MERLIN')
FONT_BIG = pg.font.SysFont('DejaVuSansMono', FONT_SIZE_BIG)
FONT_SMALL = pg.font.SysFont('DejaVuSansMono', FONT_SIZE_SMALL)
BOX_SIZE = FONT_BIG.size(' ')[1] - 2, FONT_BIG.size(' ')[1] - 2
# match types, textbox stati, game_stati
NO_MATCH = INACTIVE = LOST = UNPUSHED = 0
HALF_MATCH = ACTIVE = NEXT = PUSHED = 1
FULL_MATCH = LOCKED = WON = 2
DEBUG = 5
# # # KONSTANTS # #  #


wordle_engine = WordleEngine(hard_mode=HARD_MODE)


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


class ClickableButton:
    """A button doing something when being clicked"""
    def __init__(
            self, pos, size,
            display_icon_path, call_onclick):
        self.pos, self.size = pos, size
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

        screen.blit(self.button_surface, self.rect)

    def unpush(self):
        self.state = UNPUSHED

    def push(self):
        self.state = PUSHED
        self.call_onclick()

    def lock(self):
        self.state = LOCKED


class MsgOverlay:
    def __init__(self, msg):
        self.msg = msg
        self.visible = False
        self.text_color = Color.MSG_TEXT
        self.box_color = Color.MSG_BOX
        self.msg_surface = FONT_BIG.render(self.msg, True, self.text_color)
        self.pos = (SCREEN_SIZE[0] - self.msg_surface.get_size()[0]) / 2, (SCREEN_SIZE[1] - self.msg_surface.get_size()[1]) / 2

        self.blackout = pg.Surface(SCREEN_SIZE)
        self.blackout.set_alpha(200)
        self.blackout.fill(Color.MSG_BLACKOUT)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def set_msg(self, msg):
        self.msg = msg
        self.pos = (SCREEN_SIZE[0] - self.msg_surface.get_size()[0]) / 2, (SCREEN_SIZE[1] - self.msg_surface.get_size()[1]) / 2
        self.msg_surface = FONT_BIG.render(self.msg, True, self.text_color)

    def set_text_color(self, rgb):
        self.text_color = rgb
        self.msg_surface = FONT_BIG.render(self.msg, True, self.text_color)

    @staticmethod
    def _is_visible(func):
        def inner(self, *args, **kwargs):
            if self.visible:
                return func(self, *args, **kwargs)
        return inner

    @staticmethod
    def _blackout(func):
        def inner(self, *args, **kwargs):
            screen.blit(self.blackout, (0, 0))
            return func(self, *args, **kwargs)
        return inner

    @_is_visible
    @_blackout
    def draw(self):
        pg.draw.rect(screen, self.box_color, (self.pos, self.msg_surface.get_size()))
        screen.blit(self.msg_surface, self.pos)


def main():
    """Function containing the main level code"""
    def win():
        for box in text_boxes[1:]:
            box.lock()
        msg_win.show()

    def loose():
        text_boxes[-1].lock()
        msg_loose.show()

    def reset_all():
        for i in text_boxes:
            i.reset()
        text_boxes[0].activate()

        msg_loose.hide()
        msg_win.hide()

        wordle_engine.reset()

    game_active = True
    clock = pg.time.Clock()

    text_boxes = [InputBox((BOX_SIZE[0], (i + 1) * BOX_SIZE[0] + i * round(BOX_SIZE[0] / 2)), wordle_engine, not i) for i in range(COUNT_GUESSES)]

    reset_button = ClickableButton((0, 0), (45, 45), 'reset_icon.png', reset_all)

    msg_win = MsgOverlay(f'YOU WIN!')
    msg_win.set_text_color(Color.MSG_WIN)

    msg_loose = MsgOverlay(f'YOU LOOSE!')
    msg_loose.set_text_color(Color.MSG_LOOSE)

    while game_active:
        print(wordle_engine.letters)
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
                    if i + 1 != COUNT_GUESSES:
                        text_boxes[i + 1].activate()
                    else:
                        loose()

                elif out == LOST:
                    loose()

        # updating the screen
        screen.fill(Color.BACKGROUND)
        for box in text_boxes:
            box.draw(screen)
        reset_button.updater()
        msg_win.draw()
        msg_loose.draw()

        pg.display.update()
        clock.tick(10)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pg.quit()
        raise e
