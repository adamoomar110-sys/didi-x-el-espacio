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
                    # Iniciar con Selección de Nave
                    sound_manager.play('select')
                    self.next_state = ShipSelectionState(self.game)

    def draw(self, screen):
        screen.fill(NEGRO)
        title = self.font.render("Didi x el espacio", True, BLANCO)
        instr = self.font_small.render("Presiona ENTER para comenzar", True, BLANCO)
        screen.blit(title, (ANCHO//2 - title.get_width()//2, ALTO//3))
        screen.blit(instr, (ANCHO//2 - instr.get_width()//2, ALTO//2))

class ShipSelectionState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("Arial", 30)
        self.font_small = pygame.font.SysFont("Arial", 20)
        self.options = ["Equilibrada", "Rápida", "Pesada"]
        self.descriptions = [
            "Disparo normal, velocidad media.",
            "Disparo rápido (menos daño), muy veloz.",
            "Triple disparo, lenta pero resistente."
        ]
        self.selected_index = 0
        
        # Cargar imágenes de naves para preview
        self.ship_images = {}
        try:
            self.ship_images["Equilibrada"] = pygame.transform.scale(pygame.image.load("assets/nave_balanced.png"), (64, 80))
            self.ship_images["Rápida"] = pygame.transform.scale(pygame.image.load("assets/nave_rapid.png"), (64, 80))
            self.ship_images["Pesada"] = pygame.transform.scale(pygame.image.load("assets/nave_heavy.png"), (64, 80))
        except:
            pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    # Guardar selección
                    selection = self.options[self.selected_index]
                    if selection == "Equilibrada": contexto.ship_type = "balanced"
                    elif selection == "Rápida": contexto.ship_type = "rapid"
                    elif selection == "Pesada": contexto.ship_type = "heavy"
                    
                    sound_manager.play('select')
                    self.next_state = MapState(self.game)

    def draw(self, screen):
        screen.fill(NEGRO)
        title = self.font.render("ELIGE TU NAVE", True, BLANCO)
        screen.blit(title, (ANCHO//2 - title.get_width()//2, 50))

        for i, option in enumerate(self.options):
            color = VERDE if i == self.selected_index else BLANCO
            text = self.font.render(option, True, color)
            screen.blit(text, (100, 150 + i * 100))
            
            # Descripción y Preview
            if i == self.selected_index:
                desc = self.font_small.render(self.descriptions[i], True, (200, 200, 255))
                screen.blit(desc, (100, 190 + i * 100))
                
                # Mostrar imagen
                img = self.ship_images.get(option)
                if img:
                    screen.blit(img, (ANCHO - 200, 200))

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

        # Cargar imágenes
        self.images = {}
        file_map = {
            "Mercurio": "mercurio.png",
            "Venus": "venus.png",
            "Tierra": "tierra.png",
            "Marte": "marte.png",
            "Júpiter": "jupiter.png",
            "Saturno": "saturno.png"
        }
        for nombre, file in file_map.items():
            try:
                img = pygame.image.load(f"assets/planets/{file}")
                # Escalar según radio definido (aprox el doble del radio)
                target_r = next(p["r"] for p in self.planetas if p["nombre"] == nombre)
                img = pygame.transform.scale(img, (target_r*2, target_r*2))
                self.images[nombre] = img
            except Exception as e:
                print(f"Error cargando {file}: {e}")
                self.images[nombre] = None

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
                    sound_manager.play('select')
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
            # Dibujar planeta (Imagen o Color fallback)
            img = self.images.get(p["nombre"])
            if img:
                screen.blit(img, (p["x"] - p["r"], p["y"] - p["r"]))
            else:
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
        
        # Cargar fondo
        self.bg_image = None
        try:
            # Mapeo de nombres con tildes a archivos sin tildes si es necesario, 
            # pero aquí coinciden con los nombres de assets copiados
            fname = self.target_name.lower().replace("ú", "u") # jupiter -> jupiter
            self.bg_image = pygame.image.load(f"assets/backgrounds/bg_{fname}.png")
            self.bg_image = pygame.transform.scale(self.bg_image, (ANCHO, ALTO))
        except:
            print(f"Error loading bg for {self.target_name}")
            
        self.all_sprites = pygame.sprite.Group(self.nave)
        self.balas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        
        # Timer: 3 minutos = 180 segundos
        self.total_time = 180 # segundos
        self.timer_frames = self.total_time * FPS 
        
        # Scroll estrellas (solo si no hay imagen o para añadir profundidad)
        self.stars = []
        if not self.bg_image:
            for _ in range(50):
                self.stars.append([random.randrange(ANCHO), random.randrange(ALTO), random.randrange(1, 4)]) # x, y, speed

        self.font_hud = pygame.font.SysFont("Arial", 20)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    # Disparo
                    sound_manager.play('shoot')
                    if contexto.ship_type == "heavy":
                         # Triple disparo
                         b1 = Bala(self.nave.rect.centerx, self.nave.rect.top, direction_y=-10)
                         b2 = Bala(self.nave.rect.centerx, self.nave.rect.top, direction_x=-2, direction_y=-10)
                         b3 = Bala(self.nave.rect.centerx, self.nave.rect.top, direction_x=2, direction_y=-10)
                         self.all_sprites.add(b1, b2, b3)
                         self.balas.add(b1, b2, b3)
                    elif contexto.ship_type == "rapid":
                         # Podría tener cooldown menor, por ahora dispara normal
                         bala = Bala(self.nave.rect.centerx, self.nave.rect.top, direction_y=-12) # Bala más rápida
                         self.all_sprites.add(bala)
                         self.balas.add(bala)
                    else: # Balanced
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

        # Scroll estrellas (solo si no hay bg)
        if not self.bg_image:
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
            sound_manager.play('explosion')
            contexto.puntuacion += 10
            
        # Colisiones: Nave vs Enemigos
        hits_ship = pygame.sprite.spritecollide(self.nave, self.enemigos, True)
        if hits_ship:
            contexto.salud -= 10
            if contexto.salud <= 0:
                # Game Over logic (reset level or menu)
                # Game Over logic
                # contexto.reset_stats() # Se resetea al salir del Game Over
                self.next_state = GameOverState(self.game)

    def draw(self, screen):
        screen.fill(NEGRO)
        
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
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
        
        # Configuración de temas por planeta
        self.bg_color = (20, 20, 40) # Default
        self.plat_color = (150, 150, 150)
        
        p = contexto.planeta_actual
        if p == "Mercurio":
            self.bg_color = (50, 50, 50)
            self.plat_color = (100, 100, 100)
        elif p == "Venus":
            self.bg_color = (200, 150, 50) # Naranja atmósfera
            self.plat_color = (100, 80, 0)
        elif p == "Tierra":
            self.bg_color = (100, 200, 255) # Cielo azul
            self.plat_color = (0, 150, 0) # Pasto
        elif p == "Marte":
            self.bg_color = (200, 100, 100) # Rojizo
            self.plat_color = (150, 50, 50)
        elif p == "Júpiter":
            self.bg_color = (200, 180, 150)
            self.plat_color = (180, 120, 80)
        elif p == "Saturno":
            self.bg_color = (220, 210, 150)
            self.plat_color = (200, 180, 100)

        # Crear suelo y plataformas con nuevo color
        suelo = Plataforma(0, ALTO - 40, ANCHO, 40, color=self.plat_color)
        plat1 = Plataforma(200, 400, 200, 20, color=self.plat_color)
        plat2 = Plataforma(500, 250, 200, 20, color=self.plat_color)
        
        self.ground_enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        self.all_sprites.add(suelo, plat1, plat2)
        self.plataformas.add(suelo, plat1, plat2)
        
        # Spawn Enemigos
        e1 = GroundEnemy(300, 400, range_x=100) # En plat1
        e2 = GroundEnemy(600, ALTO - 40, range_x=200) # En el suelo
        self.ground_enemies.add(e1, e2)
        self.all_sprites.add(e1, e2)
        
        # Spawn Coleccionables
        c1 = Collectible(250, 380, "coin")
        c2 = Collectible(600, 230, "health")
        c3 = Collectible(800, ALTO - 60, "coin")
        self.collectibles.add(c1, c2, c3)
        self.all_sprites.add(c1, c2, c3)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: # Disparar
                    sound_manager.play('shoot')
                    # Determinar dirección disparo
                    dx = 10 if self.piloto.mirando_derecha else -10
                    bala = Bala(self.piloto.rect.centerx, self.piloto.rect.centery, direction_x=dx, direction_y=0, color=ROJO)
                    self.all_sprites.add(bala)
                    self.balas.add(bala)

    def update(self):
        self.piloto.update(self.plataformas)
        self.balas.update()
        self.ground_enemies.update()
        self.collectibles.update()
        
        # Colisiones: Balas vs Enemigos
        hits_enemies = pygame.sprite.groupcollide(self.ground_enemies, self.balas, True, True)
        if hits_enemies:
             sound_manager.play('explosion')
             contexto.puntuacion += 50
             
        # Colisiones: Jugador vs Enemigos
        if pygame.sprite.spritecollide(self.piloto, self.ground_enemies, False):
            contexto.salud -= 1
            # Pushback simple
            if self.piloto.velocidad_x > 0: self.piloto.rect.x -= 20
            else: self.piloto.rect.x += 20
            
            if contexto.salud <= 0:
                self.next_state = GameOverState(self.game)
                
        # Colisiones: Jugador vs Coleccionables
        hits_colex = pygame.sprite.spritecollide(self.piloto, self.collectibles, True)
        for c in hits_colex:
            sound_manager.play('collect')
            if c.type == "coin":
                contexto.puntuacion += 100
            elif c.type == "health":
                contexto.salud = min(100, contexto.salud + 20)
        
        # Simular enemigos o condiciones de victoria aquí
        if self.piloto.rect.right >= ANCHO:
            self.next_state = WinState(self.game)

        # Condición de muerte (caer al vacío)
        if self.piloto.rect.top > ALTO:
            self.next_state = GameOverState(self.game)
        
    def draw(self, screen):
        screen.fill(self.bg_color)
        self.all_sprites.draw(screen)
        
        # HUD - Barra de Vida
        pygame.draw.rect(screen, ROJO, (10, 10, 200, 20)) # Barra fondo
        pygame.draw.rect(screen, VERDE, (10, 10, 2 * contexto.salud, 20)) # Barra actual based on 100 max rect 200px
        pygame.draw.rect(screen, BLANCO, (10, 10, 200, 20), 2) # Borde
        
        # HUD - Vidas & Planeta
        font = pygame.font.SysFont("Arial", 20)
        texto_vidas = font.render(f"Vidas: {contexto.vidas} | Planeta: {contexto.planeta_actual}", True, BLANCO)
        screen.blit(texto_vidas, (10, 40))

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("Arial", 50)
        self.font_small = pygame.font.SysFont("Arial", 20)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    contexto.reset_stats()
                    self.next_state = MenuState(self.game)

    def draw(self, screen):
        screen.fill(NEGRO)
        title = self.font.render("GAME OVER", True, ROJO)
        instr = self.font_small.render("Presiona ENTER para volver al Menú", True, BLANCO)
        screen.blit(title, (ANCHO//2 - title.get_width()//2, ALTO//3))
        screen.blit(instr, (ANCHO//2 - instr.get_width()//2, ALTO//2))

class WinState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont("Arial", 50)
        self.font_small = pygame.font.SysFont("Arial", 20)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Level Up y volver al mapa
                    contexto.levelup()
                    self.next_state = MapState(self.game)

    def draw(self, screen):
        screen.fill(NEGRO)
        title = self.font.render("¡MISIÓN CUMPLIDA!", True, VERDE)
        instr = self.font_small.render("Presiona ENTER para continuar", True, BLANCO)
        screen.blit(title, (ANCHO//2 - title.get_width()//2, ALTO//3))
        screen.blit(instr, (ANCHO//2 - instr.get_width()//2, ALTO//2))
