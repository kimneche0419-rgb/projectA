import pygame
from src.entities import Player
from src.dimension import DimensionManager
from src.save_system import SaveSystem
from src.ui import MinimalistHUD
from src.settings import WINDOW_WIDTH, WINDOW_HEIGHT

class BaseLevelState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.dimension_manager = DimensionManager()
        self.save_system = SaveSystem()
        self.camera = self.state_manager.game.state_manager.game.state_manager # Will just use basic camera here for init
        from src.engine import Camera
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.player = Player(400, 300, self.dimension_manager)
        self.hud = MinimalistHUD(self.player, self.dimension_manager)
        
        self.echoes = []
        
    def enter(self):
        pass
        
    def exit(self):
        pass
        
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Manual death trigger for testing
                self.trigger_death("suicide")
                
    def trigger_death(self, cause):
        # Save exact death coordinate using the temporal echo system
        self.save_system.save_death_echo(self.player.rect.x, self.player.rect.y, cause, self.chapter_name)
        # Restart chapter
        self.state_manager.change_state(self.chapter_name)
        
    def update(self, dt):
        self.dimension_manager.update(dt)
        self.player.update(dt)
        self.camera.update(self.player.rect)
        
    def draw(self, screen):
        # Default draw order
        self.player.draw(screen, self.camera)
        
        # Render Temporal Echoes as cache/traps
        for echo in self.echoes:
            echo_rect = pygame.Rect(echo['x'], echo['y'], 20, 20)
            draw_rect = self.camera.apply(echo_rect)
            
            color = (200, 200, 0) # Gold cache if starved?
            if echo['cause'] == "laser":
                color = (255, 50, 50) # Red fire trap
                
            pygame.draw.rect(screen, color, draw_rect)
            
        self.dimension_manager.render_overlay(screen)
        self.hud.draw(screen)

class PrologueLevel(BaseLevelState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.chapter_name = "prologue"
        self.player.set_environment_physics("space")
        
        try:
            self.bg_image = pygame.image.load("assets/space_bg.png").convert()
            # Tile it or scale it to window sizes
            self.bg_image = pygame.transform.scale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print(f"Could not load background sprite: {e}")
            self.bg_image = None
        
    def enter(self):
        self.player.rect.x = 200
        self.player.rect.y = 200
        self.echoes = self.save_system.get_echoes_for_chapter(self.chapter_name)
        print(f"Loaded {len(self.echoes)} echoes for prologue.")

    def update(self, dt):
        super().update(dt)
        # Add tutorial logic here later
        
    def draw(self, screen):
        # Draw parallax background first
        if hasattr(self, 'bg_image') and self.bg_image:
            # Simple parallax trick relative to camera position
            bg_x = -(self.camera.camera.x * 0.2) % WINDOW_WIDTH
            bg_y = -(self.camera.camera.y * 0.2) % WINDOW_HEIGHT
            
            # Draw tiled background to cover screen during scrolling
            screen.blit(self.bg_image, (bg_x, bg_y))
            screen.blit(self.bg_image, (bg_x - WINDOW_WIDTH, bg_y))
            screen.blit(self.bg_image, (bg_x, bg_y - WINDOW_HEIGHT))
            screen.blit(self.bg_image, (bg_x - WINDOW_WIDTH, bg_y - WINDOW_HEIGHT))
            
        # Draw everything else
        super().draw(screen)
