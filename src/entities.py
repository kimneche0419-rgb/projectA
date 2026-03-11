import pygame
from src.settings import WINDOW_WIDTH, WINDOW_HEIGHT, PURE_WHITE, NEON_CYAN

class Entity:
    def __init__(self, x, y, width, height, color=PURE_WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = pygame.math.Vector2(0, 0)
        self.color = color
        
    def update(self, dt):
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
    def draw(self, screen, camera):
        draw_rect = camera.apply(self.rect)
        if hasattr(self, 'image') and self.image:
            screen.blit(self.image, draw_rect)
        else:
            pygame.draw.rect(screen, self.color, draw_rect)

class Player(Entity):
    def __init__(self, x, y, dimension_manager):
        super().__init__(x, y, 64, 64, NEON_CYAN)
        self.dimension_manager = dimension_manager
        self.speed = 300
        
        try:
            # Load the player ship image and scale it
            original_image = pygame.image.load("assets/player_ship.png").convert_alpha()
            self.image = pygame.transform.scale(original_image, (64, 64))
        except Exception as e:
            print(f"Could not load player sprite: {e}")
            self.image = None
        
        # Physics attributes for environment assimilation
        self.gravity = 0
        self.friction = 0.95
        
    def set_environment_physics(self, chapter_type):
        if chapter_type == "space":
            # Zero gravity, high inertia (low friction)
            self.gravity = 0
            self.friction = 0.98
        elif chapter_type == "earth":
            # High gravity, high friction (spider movement will be added later)
            self.gravity = 980
            self.friction = 0.85
        elif chapter_type == "ocean":
            # Buoyancy effect
            self.gravity = 200
            self.friction = 0.90
            
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Acceleration vector
        accel = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_w]:
            accel.y = -self.speed
        if keys[pygame.K_s]:
            accel.y = self.speed
        if keys[pygame.K_a]:
            accel.x = -self.speed
        if keys[pygame.K_d]:
            accel.x = self.speed
            
        # Apply acceleration to velocity (ignoring precise mass for now)
        self.velocity += accel * 0.016 # assume roughly 60fps dt for input accel
        
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.dimension_manager.shift()
            
    def update(self, dt):
        self.handle_input()
        
        # Apply gravity
        self.velocity.y += self.gravity * dt
        
        # Apply friction
        self.velocity *= self.friction
        
        super().update(dt)
        
        # Screen bounds collision (Temporary, until tilemap is added)
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH: self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT

class Enemy(Entity):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__(x, y, 48, 48, (255, 50, 50))
        self.velocity.x = speed_x
        self.velocity.y = speed_y
        
        try:
            original_image = pygame.image.load("assets/enemy_drone.png").convert_alpha()
            self.image = pygame.transform.scale(original_image, (48, 48))
        except Exception as e:
            print(f"Could not load enemy sprite: {e}")
            self.image = None
            
    def update(self, dt):
        super().update(dt)
        # Simple bounce behavior
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > WINDOW_HEIGHT:
            self.velocity.y *= -1
