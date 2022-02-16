# Game options and settings
from os import path

# Game properties
TITLE = "Jumpy!"
WIDTH = 550
HEIGHT = 740
FPS = 60

# Player properties
PLAYER_ACC = 0.6
PLAYER_FRIC= -0.10
PLAYER_GRAV = 0.8
JUMP_HEIGHT = -20
AUTO_JUMP = False

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# Define useful colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BG_COLOR = (56, 69, 101)
PLATFORM_COLOR = (169, 199, 169)
PLAYER_COLOR = (169, 169, 69)

# List folder directory
THIS_FILE_dir = path.dirname(__file__)
JUMPERPACK_dir = path.join(THIS_FILE_dir, "JumperPack_Kenney")
SPRITESHEETS_dir = path.join(JUMPERPACK_dir, "Spritesheets")

# Define files
HIGH_SCORE_f = "high_score.txt"
SPRITESHEET_f = "spritesheet_jumper.png"