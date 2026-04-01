# config.py
import pygame

# ENGINE SETUP
FPS = 60

#CHARACTER IMAGE
CHARACTER = "assets/player/ino.gif"

# SCREEN SETUP
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
COLOR_BG = (112, 197, 206)  

# GAME PHYSICS
GRAVITY = 0.4
FLAP_STRENGTH = -8 
MAX_FALL_SPEED = 14.5 
PIPE_SPEED = 4
MAX_PIPE_SPEED = 9 # <-- ADDED: Prevents pipes from moving too fast at high scores

# PIPE SETTINGS
HORIZONTAL_GAP = 400 
VERTICAL_GAP = 200 
COLOR_PIPE = (116, 191, 46)
COLOR_PIPE_CAP = (82, 140, 34)

# AUDIO SETTINGS
SOUND_FLAP = "assets/soundFX/tapFX.ogg"
SOUND_CRASH = "assets/soundFX/gameOver.ogg"
SOUND_START = "assets/soundFX/gameStart.ogg" 
MUSIC_BG = "assets/soundFX/backgroundMusic.ogg"