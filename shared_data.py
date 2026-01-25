
import pygame

# Configuración de pantalla
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Estado Global del Juego
class GameContext:
    def __init__(self):
        self.vidas = 3
        self.salud_max = 100
        self.salud = 100
        self.puntuacion = 0
        self.nivel_actual = 1
        self.planeta_actual = "Tierra"
        self.ship_type = "balanced" # balanced, rapid, heavy
        self.ship_level = 1
        self.planetas_visitados = []

    def reset_stats(self):
        self.salud = self.salud_max
        self.puntuacion = 0
        self.ship_type = "balanced"
        self.ship_level = 1
        
    def levelup(self):
        self.ship_level += 1
        self.salud = self.salud_max # Restaurar salud al subir de nivel

class SoundManager:
    def __init__(self):
        self.sounds = {}
        # Inicializar mixer aquí para asegurar que pygame esté listo si se llama después de init
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except:
                pass # Puede fallar si no hay audio device

        self.load_sounds()

    def load_sounds(self):
        files = {
            "shoot": "assets/sounds/shoot.wav",
            "explosion": "assets/sounds/explosion.wav",
            "jump": "assets/sounds/jump.wav",
            "collect": "assets/sounds/collect.wav",
            "select": "assets/sounds/select.wav",
        }
        for name, path in files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(0.3)
            except:
                print(f"Error loading sound {name}")
                self.sounds[name] = None

    def play(self, name):
        s = self.sounds.get(name)
        if s:
            s.play()

contexto = GameContext()
sound_manager = SoundManager()
