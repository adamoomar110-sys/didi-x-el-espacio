
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
        self.planetas_visitados = []

    def reset_stats(self):
        self.salud = self.salud_max
        # No reseteamos vidas aquí si es solo cambio de nivel, 
        # pero para reiniciar juego completo sí.

contexto = GameContext()
