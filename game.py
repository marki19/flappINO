# game.py
import pygame
import random
import sys
import config
from sprites import Player, Pipe

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier", 60, bold=True)
        self.small_font = pygame.font.SysFont("Courier", 30, bold=True)
        
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.pipe_group = pygame.sprite.Group()
        
        self.score = 0
        self.game_over = False
        self.active = False 
        self.current_speed = config.PIPE_SPEED 
        
        self.spawn_pipes() 

    def spawn_pipes(self):
        gap_y = random.randint(200, config.SCREEN_HEIGHT - 200)
        top_pipe = Pipe(config.SCREEN_WIDTH + 50, gap_y - config.VERTICAL_GAP // 2, True)
        bottom_pipe = Pipe(config.SCREEN_WIDTH + 50, gap_y + config.VERTICAL_GAP // 2, False)
        
        self.pipe_group.add(top_pipe, bottom_pipe)
        self.last_pipe_spawned = top_pipe 

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self.screen.blit(img, (x - img.get_width() // 2, y))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.game_over:
                            self.active = True 
                            self.player.flap()
                        if self.game_over:
                            self.reset_game()

            self.screen.fill(config.COLOR_BG)

            if self.active and not self.game_over:
                
                self.current_speed = config.PIPE_SPEED + (self.score // 10)

                if self.last_pipe_spawned.rect.x < config.SCREEN_WIDTH - config.HORIZONTAL_GAP:
                    self.spawn_pipes()

                if self.player.update(): 
                    self.game_over = True
                    
                self.pipe_group.update(self.current_speed)

                # PIP COLLISION CHECK
                if pygame.sprite.spritecollide(self.player, self.pipe_group, False, pygame.sprite.collide_mask):
                    self.game_over = True
                    # THE DEATH BOUNCE: Give the bird a sudden upward bump!
                    self.player.velocity = -7 

                for pipe in self.pipe_group:
                    if not hasattr(pipe, 'scored') and pipe.rect.right < self.player.rect.left:
                        if not pipe.is_top: 
                            self.score += 1
                        pipe.scored = True

            # Draw pipes (they will naturally freeze when game_over is True)
            self.pipe_group.draw(self.screen)
            
            # THE FALLING FIX: If we are dead, keep updating the bird so gravity pulls it down!
            if self.game_over:
                self.player.update()
                
            # Draw the player
            self.player_group.draw(self.screen)
            
            # Draw UI
            self.draw_text("flappINO", self.small_font, (255, 255, 255), config.SCREEN_WIDTH // 2, 20)
            self.draw_text(str(self.score), self.font, (255, 255, 255), config.SCREEN_WIDTH // 2, 60)

            if not self.active and not self.game_over:
                self.draw_text("PRESS SPACE TO START", self.small_font, (255, 255, 255), config.SCREEN_WIDTH // 2, 300)

            if self.game_over:
                self.draw_text("GAME OVER", self.font, (255, 255, 255), config.SCREEN_WIDTH // 2, 300)
                self.draw_text("PRESS SPACE TO RESTART", self.small_font, (255, 255, 255), config.SCREEN_WIDTH // 2, 360)

            pygame.display.flip()
            self.clock.tick(config.FPS)