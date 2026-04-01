# sprites.py
import pygame
import config as config

# sprites.py
import pygame
import config as config

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        raw_image = pygame.image.load(config.CHARACTER).convert_alpha()
        
        # 1. SAVE THE ORIGINAL IMAGE
        self.original_image = pygame.transform.scale(raw_image, (130, 130))
        
        # 2. Set the current image to the original
        self.image = self.original_image
        
        self.rect = self.image.get_rect(center=(200, config.SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0
        
        self.gravity = config.GRAVITY
        self.flap_strength = config.FLAP_STRENGTH

    def flap(self):
        self.velocity = self.flap_strength

    def update(self):
        self.velocity += self.gravity
        
        if self.velocity > config.MAX_FALL_SPEED:
            self.velocity = config.MAX_FALL_SPEED

        self.rect.y += self.velocity
        
        # NEW: ROTATION LOGIC
        # 1. Calculate the angle. Multiply velocity by 3 to make the tilt more dramatic.
        # (Pygame rotates counter-clockwise on positive numbers, so we invert the velocity)
        angle = -self.velocity * 3 
        
        # 2. Clamp the angle! Max tilt up is 30 degrees, Max dive down is -90 degrees.
        angle = max(min(angle, 30), -90) 
        
        # 3. Rotate from the ORIGINAL image to prevent pixel distortion
        self.image = pygame.transform.rotate(self.original_image, angle)
        
        # 4. Re-center the bounding box! Without this, the bird will wobble off-center when it rotates.
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # 5. Update the collision mask so the newly rotated shape is perfectly accurate
        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom >= config.SCREEN_HEIGHT:
            return True 
        return False

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        self.is_top = is_top 
        
        # Create a transparent surface for the pipe
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

        # Position the pipe
        if is_top:
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            self.rect = self.image.get_rect(midtop=(x, y))
            
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, current_speed):
        self.rect.x -= current_speed
        if self.rect.right < -50:
            self.kill()