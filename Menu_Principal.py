import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)

# Fuentes
title_font = pygame.font.SysFont("arial", 50)  # Fuente para el título
button_font = pygame.font.SysFont("arial", 30)  # Fuente para los botones

# Clase Botón
class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.text = text  # Texto del botón
        self.rect = pygame.Rect(x, y, w, h)  # Área del botón
        self.action = action  # Función que se ejecuta al hacer clic

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()  # Obtiene la posición del ratón

        color = GRAY  # Color por defecto del botón
        if self.rect.collidepoint(mouse_pos):  # Comprueba si el ratón está encima
            color = DARK_GRAY  # Cambia el color al pasar el ratón

        pygame.draw.rect(screen, color, self.rect)  # Dibuja el botón

        text_surf = button_font.render(self.text, True, WHITE)  # Renderiza el texto
        text_rect = text_surf.get_rect(center=self.rect.center)  # Centra el texto
        screen.blit(text_surf, text_rect)  # Dibuja el texto en el botón

    def click(self):
        if self.action:  # Comprueba si hay una acción asignada
            self.action()  # Ejecuta la acción

# Acciones de los botones
def start_game():
    print("Juego iniciado")  # Acción de ejemplo para iniciar el juego

def options():
    print("Opciones abiertas")  # Acción de ejemplo para opciones

def quit_game():
    pygame.quit()  # Cierra Pygame
    sys.exit()  # Termina el programa

# Crear botones
buttons = [
    Button("Jugar", 300, 200, 200, 60, start_game),  # Botón de jugar
    Button("Opciones", 300, 300, 200, 60, options),  # Botón de opciones
    Button("Salir", 300, 400, 200, 60, quit_game),  # Botón de salir
]

# Bucle principal
running = True
while running:
    screen.fill(BLACK)  # Rellena la pantalla con negro

    # Dibujar título
    title_text = title_font.render("MENÚ PRINCIPAL", True, WHITE)  # Crea el texto del título
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))  # Centra el título

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Detecta si se cierra la ventana
            running = False  # Detiene el bucle
            pygame.quit()  # Cierra Pygame
            sys.exit()  # Sale del programa

        if event.type == pygame.MOUSEBUTTONDOWN:  # Detecta clic del ratón
            for button in buttons:
                if button.rect.collidepoint(event.pos):  # Comprueba si se hace clic en el botón
                    button.click()  # Ejecuta la acción del botón

    # Dibujar botones
    for button in buttons:
        button.draw(screen)  # Muestra cada botón en pantalla

    pygame.display.update()  # Actualiza la pantalla en cada frame