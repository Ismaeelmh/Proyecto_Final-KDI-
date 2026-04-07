import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración de la ventana 
WIDTH, HEIGHT = 600, 650
ROWS, COLS = 8, 8
CELL_SIZE = WIDTH // COLS

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

# Colors
WHITE = (245, 255, 245)
GRAY = (144, 238, 144)
DARK_GRAY = (34, 139, 34)
BLACK = (0, 100, 0)

# Fuente
font = pygame.font.SysFont("Arial", 35)

# Función para dibujar la UI superior
def draw_ui():
    text = font.render("Buscaminas", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, 25))
    screen.blit(text, text_rect)

# Función para dibujar la cuadrícula
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + 50  # espacio para la UI

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

# Bucle principal
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_ui()
    draw_grid()

    pygame.display.update()

pygame.quit()
sys.exit()