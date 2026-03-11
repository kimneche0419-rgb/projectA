import pygame
from src.settings import WINDOW_WIDTH, WINDOW_HEIGHT

class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.active_state = None
        
        # We will initialize states later when chapters/menus are implemented
        
    def change_state(self, state_name):
        if state_name in self.states:
            if self.active_state:
                self.active_state.exit()
            self.active_state = self.states[state_name]
            self.active_state.enter()
            
    def handle_events(self, event):
        if self.active_state:
            self.active_state.handle_events(event)
            
    def update(self, dt):
        if self.active_state:
            self.active_state.update(dt)
            
    def draw(self, screen):
        if self.active_state:
            self.active_state.draw(screen)

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)
        
    def apply_parallax(self, bg_rect, parallax_factor):
        # Apply a simple parallax factor: lower factor = moves slower (background)
        offset_x = self.camera.x * parallax_factor
        offset_y = self.camera.y * parallax_factor
        return bg_rect.move((offset_x, offset_y))

    def update(self, target_rect):
        x = -target_rect.centerx + int(WINDOW_WIDTH / 2)
        y = -target_rect.centery + int(WINDOW_HEIGHT / 2)

        # Limit scrolling to map size could be added here
        
        # Smooth camera movement (Lerp)
        self.camera.x += (x - self.camera.x) * 0.1
        self.camera.y += (y - self.camera.y) * 0.1
