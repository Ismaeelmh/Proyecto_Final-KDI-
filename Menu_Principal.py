import pygame
import sys

pygame.init()  # Inicializa Pygame

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600  # Tamaño de la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crear ventana
pygame.display.set_caption("Juego")  # Título de la ventana

# Colores
WHITE = (255, 255, 255)  # Blanco
BLACK = (0, 0, 0)  # Negro
GRAY = (170, 170, 170)  # Gris claro
DARK_GRAY = (100, 100, 100)  # Gris oscuro

# Fuentes
title_font = pygame.font.SysFont("arial", 50)  # Fuente del título
button_font = pygame.font.SysFont("arial", 30)  # Fuente de botones

# Estados del juego
estado = "menu"  # Puede ser "menu" o "opciones"
modo_juego = None  # Guarda si es 1 o 2 jugadores

# Clase Botón
class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.text = text  # Texto del botón
        self.rect = pygame.Rect(x, y, w, h)  # Área del botón
        self.action = action  # Acción al hacer clic

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()  # Posición del ratón

        color = GRAY  # Color normal
        if self.rect.collidepoint(mouse_pos):  # Si el ratón está encima
            color = DARK_GRAY  # Cambia color

        pygame.draw.rect(screen, color, self.rect)  # Dibuja botón

        text_surf = button_font.render(self.text, True, WHITE)  # Renderiza texto
        text_rect = text_surf.get_rect(center=self.rect.center)  # Centra texto
        screen.blit(text_surf, text_rect)  # Dibuja texto

    def click(self):
        if self.action:
            self.action()  # Ejecuta acción

# FUNCIONES DEL MENÚ
def start_game():
    print("Iniciar juego")  # Acción de ejemplo

def abrir_opciones():
    global estado
    estado = "opciones"  # Cambia a pantalla de opciones

def salir():
    pygame.quit()  # Cierra Pygame
    sys.exit()  # Sale del programa

# FUNCIONES DE OPCIONES
def un_jugador():
    global modo_juego
    modo_juego = 1  # Selecciona 1 jugador
    print("Modo 1 jugador")

def dos_jugadores():
    global modo_juego
    modo_juego = 2  # Selecciona 2 jugadores
    print("Modo 2 jugadores")

def volver_menu():
    global estado
    estado = "menu"  # Vuelve al menú principal

# Botones del menú principal
botones_menu = [
    Button("Jugar", 300, 200, 200, 60, start_game),  # Botón jugar
    Button("Opciones", 300, 300, 200, 60, abrir_opciones),  # Botón opciones
    Button("Salir", 300, 400, 200, 60, salir),  # Botón salir
]

# Botones de opciones
botones_opciones = [
    Button("1 Jugador", 300, 200, 200, 60, un_jugador),  # Botón 1 jugador
    Button("2 Jugadores", 300, 300, 200, 60, dos_jugadores),  # Botón 2 jugadores
    Button("Volver", 300, 400, 200, 60, volver_menu),  # Botón volver
]

# Bucle principal
running = True
while running:
    screen.fill(BLACK)  # Fondo negro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Cerrar ventana
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic
            if estado == "menu":
                for boton in botones_menu:
                    if boton.rect.collidepoint(event.pos):
                        boton.click()

            elif estado == "opciones":
                for boton in botones_opciones:
                    if boton.rect.collidepoint(event.pos):
                        boton.click()

    # Dibujar pantalla según estado
    if estado == "menu":
        titulo = title_font.render("MENU PRINCIPAL", True, WHITE)  # Texto título
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 80))  # Centrar

        for boton in botones_menu:
            boton.draw(screen)  # Dibujar botones menú

    elif estado == "opciones":
        titulo = title_font.render("OPCIONES", True, WHITE)  # Texto título
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 80))  # Centrar

        for boton in botones_opciones:
            boton.draw(screen)  # Dibujar botones opciones

    pygame.display.update()  # Actualizar pantalla
