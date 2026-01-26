import pygame
from shared_data import *
from states import MenuState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(f"Didi x el espacio v{VERSION}")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Estado inicial
        self.state = MenuState(self)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Delegar manejo de eventos y actualización al estado actual
            self.state.handle_events(events)
            self.state.update()
            
            # Dibujar
            self.state.draw(self.screen)
            pygame.display.flip()
            
            # Cambiar estado si es necesario
            if self.state.next_state:
                self.state = self.state.next_state

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
