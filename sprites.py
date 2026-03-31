# sprites.py
import pygame
import config

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        raw_image = pygame.image.load("ino.gif").convert_alpha()
        self.image = pygame.transform.scale(raw_image, (150, 150))
        self.rect = self.image.get_rect(center=(200, config.SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0

    def flap(self):
        self.velocity = config.FLAP_STRENGTH

    def update(self):
        self.velocity += config.GRAVITY
        self.rect.y += self.velocity

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= config.SCREEN_HEIGHT:
            return True 
        return False

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        self.is_top = is_top # Fixes the double score bug!
        
        # 1. New Total Width: 120
        self.image = pygame.Surface((120, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # 2. New Shaft: 100 wide. 
        # To center it: (120 - 100) / 2 = 10. So we push it 10px to the right.
        shaft_rect = pygame.Rect(10, 0, 100, config.SCREEN_HEIGHT)
        pygame.draw.rect(self.image, config.COLOR_PIPE, shaft_rect)
        pygame.draw.rect(self.image, (0, 0, 0), shaft_rect, 2) 
        
        # 3. New Cap: 120 wide (matches total width)
        if is_top:
            cap_rect = pygame.Rect(0, config.SCREEN_HEIGHT - 35, 120, 35)
        else:
            cap_rect = pygame.Rect(0, 0, 120, 35)
            
        pygame.draw.rect(self.image, config.COLOR_PIPE_CAP, cap_rect)
        pygame.draw.rect(self.image, (0, 0, 0), cap_rect, 2) 

        if is_top:
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            self.rect = self.image.get_rect(midtop=(x, y))
            
        self.mask = pygame.mask.from_surface(self.image)

    # Now accepts dynamic speed so the game can get harder!
    def update(self, current_speed):
        self.rect.x -= current_speed
        if self.rect.right < -50:
            self.kill()