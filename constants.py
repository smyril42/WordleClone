import os.path
import pygame as pg
from yaml import safe_load as load_yaml


with open(str(os.path.dirname(__file__)) + '/config.yaml', 'r') as f:
    config = load_yaml(f)


# initialising pygame
pg.init()


class Constants:
    WORD_LENGTH = config['word_length']
    SCREEN_SIZE = config['screen_size_x'], config['screen_size_y']

    # fonts
    FONT_SIZE_BIG = config['font_size_big']
    FONT_BIG = pg.font.SysFont('DejaVuSansMono', FONT_SIZE_BIG)
    FONT_SIZE_SMALL = config['font_size_small']
    FONT_SMALL = pg.font.SysFont('DejaVuSansMono', FONT_SIZE_SMALL)

    # InputBox size
    BOX_SIZE = FONT_BIG.size(' ')[1] - 2, FONT_BIG.size(' ')[1] - 2

    # word lists
    VALID_ANSWERS_FP = config['valid_answers_fp']
    VALID_GUESSES_FP = config['valid_guesses_fp']

    # integer codes
    LOST = 0
    NEXT = 1
    WON = 2

    class ObjState:
        INACTIVE = 0
        ACTIVE = 1
        LOCKED = 2

    class Match:
        NONE = 0
        HALF = 1
        FULL = 2
