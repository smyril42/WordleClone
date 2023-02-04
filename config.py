# config file #
# all the following variables may be changed carefully


# do not modify __all__
__all__ = [
    'HARD_MODE', 'COUNT_GUESSES',
    'WORD_LENGTH', 'VALID_GUESSES_FP', 'VALID_ANSWERS_FP',
    'SCREEN_SIZE', 'FONT_SIZE_BIG', 'FONT_SIZE_SMALL',
    'Color'
    ]


# # #     BASIC    # # #
HARD_MODE: bool = False # default: False

COUNT_GUESSES: int = 6 # default: 6

# # # INTERMEDIATE # # #
WORD_LENGTH: int = 5 # default: 5

VALID_GUESSES_FP: str = 'valid-guesses' # default: 'valid-guesses'
VALID_ANSWERS_FP: str = 'valid-answers' # default: 'valid-answers'

# # #   ADVANCED   # # #
SCREEN_SIZE: tuple[int, int] = 450, 800 # default: (450, 800)

FONT_SIZE_BIG: int = 53 # default: 53
FONT_SIZE_SMALL: int = 26 # default: 26

# # #    COLORS    # # #
BLACK = 0, 0, 0 # default: (0, 0, 0)
GREEN = 0, 255, 0 # default: (0, 255, 0)
YELLOW = 230, 230, 140 # default: (230, 230, 140)
GRAY = 105, 105, 105 # default: (105, 105, 105)
LIGHT_GRAY = 150, 150, 150 # default: (150, 150, 150)
DARK_GRAY = 50, 50, 50 # default: (50, 50, 50)
BLUE = 0, 0, 255 # default: (0, 0, 255)
RED = 255, 0, 0 # default: (255, 0, 0)
WHITE = 255, 255, 255 # default: (255, 255, 255)

class Color:
    DEBUG = BLUE # default: BLUE

    NO_MATCH = GRAY # default: GRAY
    HALF_MATCH = YELLOW # default: YELLOW
    FULL_MATCH = GREEN # default: GREEN

    INPUT_BOX = WHITE # default: WHITE
    INPUT_LETTER = WHITE # default: WHITE

    BUTTON_PASSIVE = LIGHT_GRAY # default: LIGHT_GRAY
    BUTTON_HOVER = WHITE # default: WHITE
    BUTTON_ACTIVE = DARK_GRAY # default: DARK_GRAY

    MSG_TEXT = BLACK # default: BLACK
    MSG_BOX = WHITE # default: WHITE
    MSG_BLACKOUT = BLACK # default: BLACK

    MSG_WIN = GREEN # default: GREEN
    MSG_LOOSE = RED # default: RED

    BACKGROUND = BLACK # default: BLACK
