import pygame as pg
from config import *


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
