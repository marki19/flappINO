# game.py
import pygame
import random
import sys
import config
from sprites import Player, Pipe

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() 
        
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier", 60, bold=True)
        self.small_font = pygame.font.SysFont("Courier", 30, bold=True)
        
        # Load Audio
        self.sfx_flap = pygame.mixer.Sound(config.SOUND_FLAP)
        self.sfx_crash = pygame.mixer.Sound(config.SOUND_CRASH)
        self.sfx_start = pygame.mixer.Sound(config.SOUND_START) 
        pygame.mixer.music.load(config.MUSIC_BG)
        pygame.mixer.music.set_volume(0.4) 
        
        self.reset_game()

    def reset_game(self):
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.pipe_group = pygame.sprite.Group()
        
        self.score = 0
        self.game_over = False
        self.active = False 
        self.current_speed = config.PIPE_SPEED 
        self.death_time = 0 # NEW: Tracks when the player dies
        
        pygame.mixer.music.play(-1) 
        
        self.spawn_pipes() 

    def spawn_pipes(self):
        gap_y = random.randint(200, config.SCREEN_HEIGHT - 200)
        top_pipe = Pipe(config.SCREEN_WIDTH + 50, gap_y - config.VERTICAL_GAP // 2, True)
        bottom_pipe = Pipe(config.SCREEN_WIDTH + 50, gap_y + config.VERTICAL_GAP // 2, False)
        
        self.pipe_group.add(top_pipe, bottom_pipe)
        self.last_pipe_spawned = top_pipe 
        
    def trigger_death(self):
        # NEW: Ensure we only trigger the death logic exactly once per run
        if not self.game_over:
            self.game_over = True
            self.death_time = pygame.time.get_ticks() # Record the exact millisecond of death
            pygame.mixer.music.stop() 
            self.sfx_crash.play()     

    def draw_text(self, text, font, color, x, y):
        img = font.render(text, True, color)
        shadow = font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (x - shadow.get_width() // 2 + 2, y + 2))
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
                            if not self.active: 
                                self.active = True 
                                self.sfx_start.play() 
                            else:
                                self.sfx_flap.play() 
                                
                            self.player.flap()
                            
                        elif self.game_over:
                            # NEW: Only allow restart if 1000 milliseconds (1 second) have passed since death
                            current_time = pygame.time.get_ticks()
                            if current_time - self.death_time > 1000:
                                self.reset_game()

            self.screen.fill(config.COLOR_BG)

            if self.active and not self.game_over:
                self.current_speed = config.PIPE_SPEED + (self.score // 10)

                if self.last_pipe_spawned.rect.x < config.SCREEN_WIDTH - config.HORIZONTAL_GAP:
                    self.spawn_pipes()

                if self.player.update(): 
                    self.trigger_death()
                    
                self.pipe_group.update(self.current_speed)

                if pygame.sprite.spritecollide(self.player, self.pipe_group, False, pygame.sprite.collide_mask):
                    self.trigger_death()
                    self.player.velocity = -7 

                for pipe in self.pipe_group:
                    if not hasattr(pipe, 'scored') and pipe.rect.right < self.player.rect.left:
                        if not pipe.is_top: 
                            self.score += 1
                        pipe.scored = True

            self.pipe_group.draw(self.screen)
            
            if self.game_over:
                self.player.update()
                
            self.player_group.draw(self.screen)
            
            self.draw_text("flappINO", self.small_font, (255, 255, 255), config.SCREEN_WIDTH // 2, 20)
            self.draw_text(str(self.score), self.font, (255, 255, 255), config.SCREEN_WIDTH // 2, 60)

            if not self.active and not self.game_over:
                self.draw_text("PRESS SPACE TO START", self.small_font, (255, 255, 255), config.SCREEN_WIDTH // 2, 300)

            if self.game_over:
                # NEW: Only show the "PRESS SPACE TO RESTART" text if the cooldown is actually finished!
                self.draw_text("GAME OVER", self.font, (255, 255, 255), config.SCREEN_WIDTH // 2, 300)
                if pygame.time.get_ticks() - self.death_time > 1000:
                    self.draw_text("PRESS SPACE TO RESTART", self.small_font, (255, 255, 255), config.SCREEN_WIDTH // 2, 360)

            pygame.display.flip()
            self.clock.tick(config.FPS)