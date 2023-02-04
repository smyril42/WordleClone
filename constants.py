import pygame as pg
import yaml
from colors import Color

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

WORD_LENGTH = config['word_length']
SCREEN_SIZE = config['screen_size_x'], config['screen_size_y']

VALID_ANSWERS_FP = config['valid_answers_fp']
VALID_GUESSES_FP = config['valid_guesses_fp']

FONT_SIZE_BIG = config['font_size_big']
FONT_SIZE_SMALL = config['font_size_small']


# initialising pygame
pg.init()


# fonts
FONT_BIG = pg.font.SysFont('DejaVuSansMono', FONT_SIZE_BIG)
FONT_SMALL = pg.font.SysFont('DejaVuSansMono', FONT_SIZE_SMALL)

# InputBox size
BOX_SIZE = FONT_BIG.size(' ')[1] - 2, FONT_BIG.size(' ')[1] - 2

# integer codes
NO_MATCH = INACTIVE = LOST = UNPUSHED = 0
HALF_MATCH = ACTIVE = NEXT = PUSHED = 1
FULL_MATCH = LOCKED = WON = 2
DEBUG = 5
