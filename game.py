# game.py
import turtle
import time
import sys
import random

import config
from sprites import Player, Pipe, ScoreBoard

class Game:
    def __init__(self):
        # --- SCREEN SETUP ---
        self.wn = turtle.Screen()
        self.wn.bgcolor(config.COLOR_BG) 
        self.wn.title("OOP Flappy Bird - flappINO")
        self.wn.setup(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
        self.wn.tracer(0)
        self.wn.register_shape("ino.gif") 

        # --- GAME STATE ---
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.frame_count = 0

        # --- INITIALIZATION ---
        self.player = Player(-100, 0)
        self.scoreboard = ScoreBoard()
        self.scoreboard.draw_live_score(self.score)
        
        self.spawn_pipe_pair()
        self.setup_controls()

    def spawn_pipe_pair(self):
        min_y = -150
        max_y = 150
        center_y = random.randint(min_y, max_y)
        
        top_pipe_y = center_y + (config.GAP_SIZE / 2) + 300
        top_cap_y = center_y + (config.GAP_SIZE / 2) + 15
        
        bottom_pipe_y = center_y - (config.GAP_SIZE / 2) - 300
        bottom_cap_y = center_y - (config.GAP_SIZE / 2) - 15
        
        self.pipes.append(Pipe(config.PIPE_SPAWN_X, top_pipe_y, True, top_cap_y))
        self.pipes.append(Pipe(config.PIPE_SPAWN_X, bottom_pipe_y, False, bottom_cap_y))

    def handle_flap(self):
        if not self.game_over:
            self.player.flap()

    def restart(self):
        if self.game_over:
            self.player.goto(-100, 0)
            self.player.dy = 0
            self.player.setheading(0)
            
            for pipe in self.pipes:
                pipe.hide()
            self.pipes.clear()
            
            self.score = 0
            self.scoreboard.draw_live_score(self.score)
            self.spawn_pipe_pair()
            self.frame_count = 0
            self.game_over = False

    def exit_game(self):
        self.wn.bye()
        sys.exit()

    def setup_controls(self):
        turtle.listen()
        turtle.onkeypress(self.handle_flap, "space")
        turtle.onkeypress(self.handle_flap, "w")
        turtle.onkeypress(self.handle_flap, "W")
        turtle.onkeypress(self.handle_flap, "Up")
        turtle.onkeypress(self.restart, "r")
        turtle.onkeypress(self.restart, "R")
        turtle.onkeypress(self.exit_game, "Escape")

    def run(self):
        # --- MAIN GAME LOOP ---
        while True:
            frame_start_time = time.perf_counter()
            
            if not self.game_over:
                # 1. Update Player 
                if self.player.update():
                    self.game_over = True
                    
                # 2. Update Pipes & Check Collisions
                for pipe in self.pipes[:]:
                    pipe.update()
                    
                    if pipe.is_collision(self.player):
                        self.game_over = True
                        
                    if not pipe.passed and pipe.logical_x < self.player.xcor() and not pipe.is_top:
                        self.score += 1
                        pipe.passed = True
                        
                    if pipe.logical_x < config.PIPE_DESPAWN_X:
                        pipe.hide()
                        self.pipes.remove(pipe)

                # 3. Handle Rendering & Game State
                if self.game_over:
                    self.scoreboard.show_game_over()
                else:
                    self.scoreboard.draw_live_score(self.score)
                    
                    self.frame_count += 1
                    if self.frame_count >= 80:
                        self.spawn_pipe_pair()
                        self.frame_count = 0
                        
            self.wn.update()
            
            frame_duration = time.perf_counter() - frame_start_time
            if frame_duration < config.FRAME_TIME:
                time.sleep(config.FRAME_TIME - frame_duration)