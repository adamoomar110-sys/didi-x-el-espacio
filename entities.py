import pygame
from shared_data import *

# --- CLASES COMUNES ---
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x=0, direction_y=-10, color=AMARILLO):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dx = direction_x
        self.dy = direction_y

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Eliminar si sale de pantalla
        if (self.rect.bottom < 0 or self.rect.top > ALTO or 
            self.rect.left < 0 or self.rect.right > ANCHO):
            self.kill()

# --- CLASES MODO ESPACIO ---
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            # Seleccionar imagen según tipo
            if contexto.ship_type == "rapid": fname = "nave_rapid.png"
            elif contexto.ship_type == "heavy": fname = "nave_heavy.png"
            else: fname = "nave_balanced.png"
            
            self.image = pygame.image.load(f"assets/{fname}")
            self.image = pygame.transform.scale(self.image, (40, 50))
        except:
             self.image = pygame.Surface((40, 50))
             self.image.fill(AZUL) 
        
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad_x = 0
        self.velocidad_y = 0

    def update(self):
        self.velocidad_x = 0
        self.velocidad_y = 0
        teclas = pygame.key.get_pressed()
        
        # Movimiento libre en modo espacio
        # Factor de nivel: +10% velocidad por nivel
        level_mult = 1 + (contexto.ship_level - 1) * 0.1
        
        base_speed = 6
        if contexto.ship_type == "rapid": base_speed = 9
        elif contexto.ship_type == "heavy": base_speed = 4
        
        speed = base_speed * level_mult

        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -speed
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = speed
        if teclas[pygame.K_UP]:
            self.velocidad_y = -speed
        if teclas[pygame.K_DOWN]:
            self.velocidad_y = speed
        
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Mantener dentro de pantalla
        if self.rect.right > ANCHO: self.rect.right = ANCHO
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.bottom > ALTO: self.rect.bottom = ALTO
        if self.rect.top < 0: self.rect.top = 0

class Planeta(pygame.sprite.Sprite):
    def __init__(self, x, y, nombre, color, radio=40):
        super().__init__()
        self.nombre = nombre
        self.radio = radio
        self.image = pygame.Surface((radio*2, radio*2))
        self.image.set_colorkey(NEGRO) # Hacer transparente el fondo del cuadrado
        pygame.draw.circle(self.image, color, (radio, radio), radio)
        # Anillo simple para estética si es Saturno (ejemplo)
        if nombre == "Saturno":
             pygame.draw.ellipse(self.image, (200, 200, 200), (0, radio//2, radio*2, radio), 2)
             
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.mask = pygame.mask.from_surface(self.image) # Para colisiones más precisas si se necesita

# --- CLASES MODO PLATAFORMA ---
class Piloto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = ALTO - 150
        
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.en_suelo = False
        self.mirando_derecha = True

    def update(self, plataformas):
        # 1. Movimiento lateral
        self.velocidad_x = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -5
            self.mirando_derecha = False
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 5
            self.mirando_derecha = True
            
        # 2. Salto
        if teclas[pygame.K_SPACE] and self.en_suelo:
            sound_manager.play('jump')
            self.velocidad_y = -15
            self.en_suelo = False
            
        # 3. Gravedad
        self.velocidad_y += 0.8 # Gravedad
        
        # 4. Aplicar movimiento y colisiones
        self.rect.x += self.velocidad_x
        # (Aquí irían colisiones horizontales si hubiera paredes complejas)
        
        self.rect.y += self.velocidad_y
        
        # Colisiones con plataformas (suelo)
        self.en_suelo = False
        hits = pygame.sprite.spritecollide(self, plataformas, False)
        for plat in hits:
            if self.velocidad_y > 0: # Cayendo
                self.rect.bottom = plat.rect.top
                self.velocidad_y = 0
                self.en_suelo = True
        
        # Límite inferior (muerte o reset posición)
        if self.rect.top > ALTO:
            self.rect.y = 0 # Caída al vacío (temporal)

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=(150, 150, 150)):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type="coin"):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        if type == "coin":
            self.image.fill(AMARILLO)
            pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 8)
        elif type == "health":
            self.image.fill(VERDE)
            pygame.draw.cross(self.image, BLANCO, (10, 10), 10, 4)
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
    def update(self):
        pass # Podría tener animación simple aquí
