"""
A Clone of the viral game Wordle.
by Merlin Pritlove

Run: main()
"""

# pylint: disable=[E1101, E1102, E0213, C0116]

import pygame as pg
from wordle_engine import WordleEngine
from input_box import InputBox
from clickable_button import ClickableButton
from msg_overlay import MsgOverlay
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

    wordle_engine = WordleEngine(hard_mode=HARD_MODE)

    game_active = True
    clock = pg.time.Clock()

    text_boxes = [InputBox((BOX_SIZE[0], (i + 1) * BOX_SIZE[0] + i * round(BOX_SIZE[0] / 2)), wordle_engine, not i) for i in range(COUNT_GUESSES)]

    reset_button = ClickableButton((0, 0), (45, 45), screen, 'reset_icon.png', reset_all)

    msg_win = MsgOverlay(f'YOU WIN!', screen)
    msg_win.set_text_color(Color.MSG_WIN)

    msg_loose = MsgOverlay(f'YOU LOOSE!', screen)
    msg_loose.set_text_color(Color.MSG_LOOSE)

    while game_active:
        print(wordle_engine.letters)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_active = False
                pg.quit()
                return True

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
