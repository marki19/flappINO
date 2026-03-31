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
PIPE_SPEED = 4 # Starting speed (Slightly slower and more manageable)

# PIPE SETTINGS
HORIZONTAL_GAP = 400 # The exact distance between pipes (fixes the unusual gap!)
VERTICAL_GAP = 200 # The hole the bird flies through
COLOR_PIPE = (116, 191, 46)
COLOR_PIPE_CAP = (82, 140, 34)