import pygame

WINDOW_WIDTH = 736
WINDOW_HEIGHT = 480
PIXEL = 32

COLS = WINDOW_WIDTH // PIXEL
ROWS = WINDOW_WIDTH // PIXEL


BACKGROUND = (255, 255, 255)
BATTLESHIP_COLOR = (255, 0, 0)
WITHOUT_BATTLESHIP = (0, 0, 0)

PLAYER_BACKGROUD = "assets/background/radargrid.png"
COOP_BACKGROUND = "assets/background/oceangrid.png"

BATTLE_SHIP1X2 = "assets/battle_ship/ship1x2.png"
BATTLE_SHIP1X3_1 = "assets/battle_ship/ship1x3_1.png"
BATTLE_SHIP1X3_2 = "assets/battle_ship/ship1x3_2.png"
BATTLE_SHIP1X4 = "assets/battle_ship/ship1x4.png"
BATTLE_SHIP1X5 = "assets/battle_ship/ship1x5.png"

# icon
TOKEN_GREEN_HIT = "assets/tokens/hit-1.png"
TOKEN_GREEN_MISS = "assets/tokens/miss-1.png"
# frames
TOKEN_GREEN_MISS_LIST = "assets/animation/player_token/miss/"
TOKEN_GREEN_HIT_LIST = "assets/animation/player_token/hit/"

# icon
TOKEN_BLUE_HIT = "assets/tokens/hit-2.png"
TOKEN_BLUE_MISS = "assets/tokens/miss-2.png"

# frames
TOKEN_BLUE_MISS_LIST = "assets/animation/coop_token/miss/"
TOKER_BLUE_HIT_LIST = "assets/animation/coop_token/hit/"

# icon
TOKEN_TRANSPARENT = "assets/tokens/transparent.png"

RADAR_LIST = "assets/animation/radar/"

RADAR_BUTTON = "assets/button/button.png"