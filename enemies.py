import pygame
import random
from shared_data import *

class SpaceEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("assets/enemy_space.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.image.set_colorkey(NEGRO)
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill(ROJO)
            
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

class GroundEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, range_x=100):
        super().__init__()
        try:
             self.image = pygame.image.load("assets/enemy_ground.png")
             self.image = pygame.transform.scale(self.image, (30, 30))
             self.image.set_colorkey(NEGRO)
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill((200, 50, 50)) # Rojo oscuro
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        
        self.start_x = x
        self.range_x = range_x
        self.speed = 2
        self.direction = 1 # 1 derecha, -1 izquierda

    def update(self):
        self.rect.x += self.speed * self.direction
        
        # Patrullar rango
        if self.rect.x > self.start_x + self.range_x:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1
