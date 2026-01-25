import pygame
import random
from shared_data import *

class SpaceEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(ROJO)
        # Dibujar algo para que parezca nave enemiga
        pygame.draw.circle(self.image, (200, 0, 0), (15, 15), 10)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(2, 6)
        self.speed_x = random.randrange(-2, 3)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Rebote en bordes laterales
        if self.rect.right > ANCHO or self.rect.left < 0:
            self.speed_x *= -1
            
        # Eliminar si sale por abajo
        if self.rect.top > ALTO:
            self.kill()
