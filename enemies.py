import pygame
import random
from shared_data import *
from entities import Bala

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

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Intentar cargar imagen o usar un rectángulo grande
        try:
            self.image = pygame.image.load("assets/boss.png")
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.image.set_colorkey(NEGRO)
        except:
            self.image = pygame.Surface((100, 100))
            self.image.fill((100, 0, 100)) # Violeta oscuro
            # Ojos amenazantes
            pygame.draw.rect(self.image, ROJO, (20, 30, 20, 10))
            pygame.draw.rect(self.image, ROJO, (60, 30, 20, 10))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed_y = 2
        self.direction_y = 1
        self.health = 500 # Mucha vida
        self.max_health = 500
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1500 # Dispara cada 1.5 segundos

    def update(self):
        # Movimiento vertical (flotar)
        self.rect.y += self.speed_y * self.direction_y
        
        if self.rect.top < 50 or self.rect.bottom > ALTO - 50:
            self.direction_y *= -1
            
    def try_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # Disparar hacia la izquierda (asumiendo que el jugador viene de la izquierda)
            return Bala(self.rect.centerx, self.rect.centery, direction_x=-8, direction_y=0, color=(255, 0, 255))
        return None

    def draw_health(self, screen):
        # Barra de vida del jefe en la parte superior
        width = 400
        height = 20
        x = (ANCHO - width) // 2
        y = 50
        
        # Fondo
        pygame.draw.rect(screen, NEGRO, (x, y, width, height))
        # Vida actual
        fill_width = (self.health / self.max_health) * width
        pygame.draw.rect(screen, ROJO, (x, y, fill_width, height))
        # Borde
        pygame.draw.rect(screen, BLANCO, (x, y, width, height), 2)
        
        font = pygame.font.SysFont("Arial", 16)
        text = font.render("JEFE PLANETARIO", True, BLANCO)
        screen.blit(text, (x + width//2 - text.get_width()//2, y - 20))
