import pygame
import random
import math

# Colores para efectos
CYAN_GLOW = (0, 255, 255)
ORANGE_FIRE = (255, 100, 0)
WHITE = (255, 255, 255)
PURPLE_MAGIC = (200, 50, 255)

class Particle:
    def __init__(self, x, y, dx, dy, color, size, life):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1
        self.size = max(0, self.size - 0.1) # Shrink over time

    def draw(self, surface):
        if self.life > 0 and self.size > 0:
            # Calcular alpha basado en vida
            alpha = int((self.life / self.max_life) * 255)
            
            # Crear superficie para partícula con blend
            surf = pygame.Surface((int(self.size)*2, int(self.size)*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (int(self.size), int(self.size)), int(self.size))
            
            # Blit con additive blend para "Glow"
            surface.blit(surf, (int(self.x - self.size), int(self.y - self.size)), special_flags=pygame.BLEND_ADD)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, p):
        self.particles.append(p)

    def update(self):
        # Update particles and remove dead ones
        self.particles = [p for p in self.particles if p.life > 0 and p.size > 0]
        for p in self.particles:
            p.update()

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def create_explosion(self, x, y, color=ORANGE_FIRE, count=20):
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(1, 5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            size = random.uniform(2, 6)
            life = random.randint(20, 40)
            self.add_particle(Particle(x, y, dx, dy, color, size, life))

    def create_thruster_trail(self, x, y, color=CYAN_GLOW):
        # Particles moviéndose hacia abajo (opuesto a la nave)
        dx = random.uniform(-1, 1)
        dy = random.uniform(2, 5)
        size = random.uniform(2, 5)
        life = random.randint(10, 20)
        self.add_particle(Particle(x, y, dx, dy, color, size, life))
        
    def create_sparkle(self, x, y, color=WHITE):
        for _ in range(10):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(0.5, 2)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            size = random.uniform(1, 3)
            life = random.randint(10, 30)
            self.add_particle(Particle(x, y, dx, dy, color, size, life))

    def create_bullet_trail(self, x, y, color=WHITE):
        size = random.uniform(2, 4)
        life = random.randint(5, 10)
        self.add_particle(Particle(x, y, 0, 0, color, size, life))
