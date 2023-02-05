"""
A Clone of the viral game Wordle.
by Merlin Pritlove

Run: main()
"""

# pylint: disable=[E1101, E1102, E0213, C0116]

import pygame as pg
from argparse import ArgumentParser
from wordle_engine.wordle_engine import WordleEngine
from input_box import InputBox
from clickable_button import ClickableButton
from msg_overlay import MsgOverlay
import constants as const
from constants import Color


arg_parser = ArgumentParser(description='A Clone of the viral game Wordle. by Merlin Pritlove')
arg_parser.add_argument('-H', '--Hard',
                        action='store_true',
                        help='activate hard mode')
arg_parser.add_argument('-g', '--guesses',
                        action='store', type=int, default=6,
                        help='set the number of allowed guesses per game')

args = arg_parser.parse_args()


# initialising pygame
pg.init()


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

    screen = pg.display.set_mode(const.SCREEN_SIZE)
    pg.display.set_caption('PLAY WORDLE | BY MERLIN')

    wordle_engine = WordleEngine(hard_mode=args.Hard)

    clock = pg.time.Clock()

    text_boxes = [InputBox((const.BOX_SIZE[0], (i + 1) * const.BOX_SIZE[0] + i * round(const.BOX_SIZE[0] / 2)), wordle_engine, not i) for i in range(args.guesses)]

    reset_button = ClickableButton((0, 0), (45, 45), screen, 'reset_icon.png', reset_all)

    msg_win = MsgOverlay('YOU WIN!', screen, Color.MSG_WIN)

    msg_loose = MsgOverlay('YOU LOOSE!', screen, Color.MSG_LOOSE)

    while True:
        print(wordle_engine.letters)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return True

            for i, box in enumerate(text_boxes):
                out = box.event_handler(event)
                if out == const.WON:
                    win()
                elif out == const.NEXT:
                    if i + 1 != args.guesses:
                        text_boxes[i + 1].activate()
                    else:
                        loose()

                elif out == const.LOST:
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
