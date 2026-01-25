import pygame
import random
from shared_data import *
from entities import *
from enemies import *

class GameState:
    def __init__(self, game):
        self.game = game
        self.next_state = None

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("Arial", 40)
        self.font_small = pygame.font.SysFont("Arial", 20)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Iniciar con Selección de Mapa
                    self.next_state = MapState(self.game)

    def draw(self, screen):
        screen.fill(NEGRO)
        title = self.font.render("Didi x el espacio", True, BLANCO)
        instr = self.font_small.render("Presiona ENTER para comenzar", True, BLANCO)
        screen.blit(title, (ANCHO//2 - title.get_width()//2, ALTO//3))
        screen.blit(instr, (ANCHO//2 - instr.get_width()//2, ALTO//2))

class MapState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Definir Sistema Solar (Alineados Horizontalmente)
        self.y_align = ALTO // 2
        self.planetas = [
            {"nombre": "Mercurio", "color": (169, 169, 169), "x": 150, "y": self.y_align, "r": 15},
            {"nombre": "Venus", "color": (255, 198, 73), "x": 250, "y": self.y_align, "r": 20},
            {"nombre": "Tierra", "color": (0, 0, 255), "x": 350, "y": self.y_align, "r": 22},
            {"nombre": "Marte", "color": (255, 0, 0), "x": 450, "y": self.y_align, "r": 18},
            {"nombre": "Júpiter", "color": (210, 180, 140), "x": 600, "y": self.y_align, "r": 45},
            {"nombre": "Saturno", "color": (238, 232, 170), "x": 750, "y": self.y_align, "r": 40},
        ]
        self.selected_index = 0
        self.font_ui = pygame.font.SysFont("Arial", 20)
        self.font_title = pygame.font.SysFont("Arial", 30)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected_index = (self.selected_index + 1) % len(self.planetas)
                elif event.key == pygame.K_LEFT:
                    self.selected_index = (self.selected_index - 1) % len(self.planetas)
                elif event.key == pygame.K_RETURN:
                    # Seleccionar planeta e iniciar viaje
                    target_planet = self.planetas[self.selected_index]
                    contexto.planeta_actual = target_planet["nombre"]
                    self.next_state = SpaceTravelState(self.game, target_planet)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(NEGRO)
        title = self.font_title.render("SELECCIONA TU DESTINO", True, BLANCO)
        screen.blit(title, (ANCHO//2 - title.get_width()//2, 20))

        # Dibujar Sol (Izquierda borde)
        pygame.draw.circle(screen, AMARILLO, (0, self.y_align), 80)
        # Resplandor
        pygame.draw.circle(screen, (255, 200, 0), (0, self.y_align), 90, 2)

        for i, p in enumerate(self.planetas):
            # Dibujar planeta
            pygame.draw.circle(screen, p["color"], (p["x"], p["y"]), p["r"])
            
            # Dibujar selección (Cursor)
            if i == self.selected_index:
                pygame.draw.circle(screen, VERDE, (p["x"], p["y"]), p["r"] + 5, 2)
                
            # Nombre
            txt = self.font_ui.render(p["nombre"], True, BLANCO)
            screen.blit(txt, (p["x"] - txt.get_width()//2, p["y"] + p["r"] + 10))


class SpaceTravelState(GameState):
    def __init__(self, game, target_planet_data):
        super().__init__(game)
        self.target_name = target_planet_data["nombre"]
        self.nave = Nave()
        self.nave.rect.bottom = ALTO - 20 # Empezar abajo
        
        self.all_sprites = pygame.sprite.Group(self.nave)
        self.balas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        
        # Timer: 3 minutos = 180 segundos
        self.total_time = 180 # segundos
        self.timer_frames = self.total_time * FPS 
        
        # Scroll fondo
        self.stars = []
        for _ in range(50):
            self.stars.append([random.randrange(ANCHO), random.randrange(ALTO), random.randrange(1, 4)]) # x, y, speed

        self.font_hud = pygame.font.SysFont("Arial", 20)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    # Disparo
                    bala = Bala(self.nave.rect.centerx, self.nave.rect.top, direction_y=-10)
                    self.all_sprites.add(bala)
                    self.balas.add(bala)

    def update(self):
        # Timer
        self.timer_frames -= 1
        if self.timer_frames <= 0:
            # LLegada al planeta
            self.next_state = PlanetState(self.game)
            return

        # Scroll estrellas
        for s in self.stars:
            s[1] += s[2] * 2 # Mover hacia abajo
            if s[1] > ALTO:
                s[1] = 0
                s[0] = random.randrange(ANCHO)
        
        # Spawn Enemigos
        if random.random() < 0.02: # 2% chance por frame
            enemy = SpaceEnemy()
            self.all_sprites.add(enemy)
            self.enemigos.add(enemy)

        self.all_sprites.update()
        
        # Colisiones: Balas vs Enemigos
        hits = pygame.sprite.groupcollide(self.enemigos, self.balas, True, True)
        for hit in hits:
            contexto.puntuacion += 10
            
        # Colisiones: Nave vs Enemigos
        hits_ship = pygame.sprite.spritecollide(self.nave, self.enemigos, True)
        if hits_ship:
            contexto.salud -= 10
            if contexto.salud <= 0:
                # Game Over logic (reset level or menu)
                contexto.reset_stats() # Simple reset por ahora
                self.next_state = MenuState(self.game)

    def draw(self, screen):
        screen.fill(NEGRO)
        
        # Dibujar estrellas (efecto velocidad)
        for s in self.stars:
            pygame.draw.circle(screen, (200, 200, 255), (s[0], s[1]), 2)
            
        self.all_sprites.draw(screen)
        
        # HUD
        mins = int((self.timer_frames / FPS) // 60)
        secs = int((self.timer_frames / FPS) % 60)
        timer_text = f"TIEMPO: {mins:02}:{secs:02} | DESTINO: {self.target_name.upper()}"
        
        score_text = f"PUNTOS: {contexto.puntuacion} | SALUD: {contexto.salud}%"
        
        txt_surf = self.font_hud.render(timer_text, True, AMARILLO)
        screen.blit(txt_surf, (ANCHO//2 - txt_surf.get_width()//2, 10))
        
        score_surf = self.font_hud.render(score_text, True, BLANCO)
        screen.blit(score_surf, (10, ALTO - 30))

class PlanetState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.piloto = Piloto()
        self.all_sprites = pygame.sprite.Group(self.piloto)
        self.plataformas = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        
        # Crear suelo y plataformas
        suelo = Plataforma(0, ALTO - 40, ANCHO, 40)
        plat1 = Plataforma(200, 400, 200, 20)
        plat2 = Plataforma(500, 250, 200, 20)
        
        self.all_sprites.add(suelo, plat1, plat2)
        self.plataformas.add(suelo, plat1, plat2)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # Disparar
                    # Determinar dirección disparo
                    dx = 10 if self.piloto.mirando_derecha else -10
                    bala = Bala(self.piloto.rect.centerx, self.piloto.rect.centery, direction_x=dx, direction_y=0, color=ROJO)
                    self.all_sprites.add(bala)
                    self.balas.add(bala)

    def update(self):
        self.piloto.update(self.plataformas)
        self.balas.update()
        
        # Simular enemigos o condiciones de victoria aquí
        
    def draw(self, screen):
        screen.fill((20, 20, 40)) # Azul oscuro cielo planeta
        self.all_sprites.draw(screen)
        
        # HUD - Barra de Vida
        pygame.draw.rect(screen, ROJO, (10, 10, 200, 20)) # Barra fondo
        pygame.draw.rect(screen, VERDE, (10, 10, 2 * contexto.salud, 20)) # Barra actual based on 100 max rect 200px
        pygame.draw.rect(screen, BLANCO, (10, 10, 200, 20), 2) # Borde
        
        # HUD - Vidas & Planeta
        font = pygame.font.SysFont("Arial", 20)
        texto_vidas = font.render(f"Vidas: {contexto.vidas} | Planeta: {contexto.planeta_actual}", True, BLANCO)
        screen.blit(texto_vidas, (10, 40))
