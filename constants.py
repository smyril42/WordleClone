import pygame as pg
from settings import HARD_MODE
from settings import COUNT_GUESSES
from settings import WORD_LENGTH
from settings import VALID_ANSWERS_FP, VALID_GUESSES_FP
from settings import SCREEN_SIZE
from settings import FONT_SIZE_BIG, FONT_SIZE_SMALL

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
