# config.py
import pygame

# ENGINE SETUP
FPS = 60

# SCREEN SETUP
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
COLOR_BG = (112, 197, 206)  

# GAME PHYSICS
GRAVITY = 0.4
FLAP_STRENGTH = -8 
PIPE_SPEED = 4 

# PIPE SETTINGS
HORIZONTAL_GAP = 400 
VERTICAL_GAP = 200 
COLOR_PIPE = (116, 191, 46)
COLOR_PIPE_CAP = (82, 140, 34)

# AUDIO SETTINGS
SOUND_FLAP = "soundFX/tapFX.mp3"
SOUND_CRASH = "soundFX/gameOver.mp3"
SOUND_START = "soundFX/gameStart.mp3" # <-- Added the new start sound here!
MUSIC_BG = "soundFX/backgroundMusic.mp3"