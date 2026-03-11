import pygame
from src.settings import WINDOW_WIDTH, WINDOW_HEIGHT, NEON_CYAN, NEON_MAGENTA
from src.dimension import DimensionState

class MinimalistHUD:
    def __init__(self, player, dimension_manager):
        self.player = player
        self.dimension_manager = dimension_manager
        
    def draw(self, screen):
        # We can draw everything attached to the screen center or player
        # Let's draw a Holo-ring at the screen center (since camera centers on player)
        
        center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        radius = 50
        
        # Determine color based on Dimension
        if self.dimension_manager.get_dimension() == DimensionState.PHYSICAL:
            color = NEON_CYAN
        else:
            color = NEON_MAGENTA
            
        # Draw Holo-ring
        pygame.draw.circle(screen, color, center, radius, width=2)
        
        # Display Dimension Text
        font = pygame.font.SysFont("Courier", 18, bold=True)
        text_surf = font.render(f"DIM: {self.dimension_manager.get_dimension().name}", True, color)
        screen.blit(text_surf, (20, 20))
        
        # Temporarily show coordinates
        coord_surf = font.render(f"POS: {int(self.player.rect.x)}, {int(self.player.rect.y)}", True, (200, 200, 200))
        screen.blit(coord_surf, (20, 50))
