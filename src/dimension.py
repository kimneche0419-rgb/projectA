from enum import Enum
import pygame

class DimensionState(Enum):
    PHYSICAL = 1
    VOID = 2

class DimensionManager:
    def __init__(self):
        self.current_dimension = DimensionState.PHYSICAL
        self.shift_cooldown = 0
        self.max_cooldown = 0.5  # seconds
    
    def shift(self):
        if self.shift_cooldown <= 0:
            if self.current_dimension == DimensionState.PHYSICAL:
                self.current_dimension = DimensionState.VOID
            else:
                self.current_dimension = DimensionState.PHYSICAL
            self.shift_cooldown = self.max_cooldown
            return True
        return False

    def update(self, dt):
        if self.shift_cooldown > 0:
            self.shift_cooldown -= dt
            
    def get_dimension(self):
        return self.current_dimension
        
    def render_overlay(self, screen):
        # Temporary placeholder for dimension visual effect (e.g. Neon scanlines or tint)
        if self.current_dimension == DimensionState.VOID:
            # Add a slight purple tint or edge vignette
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((75, 0, 130, 40)) # Translucent purple
            screen.blit(overlay, (0, 0))
