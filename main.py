import pygame
import sys
from src.settings import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, TITLE
from src.engine import GameStateManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.state_manager = GameStateManager(self)
        
        # Register game states
        from src.levels import PrologueLevel
        self.state_manager.states['prologue'] = PrologueLevel(self.state_manager)
        
        # Start game
        self.state_manager.change_state('prologue')
        
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.events()
            self.update(dt)
            self.draw()
            
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            self.state_manager.handle_events(event)
            
    def update(self, dt):
        self.state_manager.update(dt)
        
    def draw(self):
        self.screen.fill((0, 0, 0)) # Default background
        self.state_manager.draw(self.screen)
        pygame.display.flip()
        
    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
