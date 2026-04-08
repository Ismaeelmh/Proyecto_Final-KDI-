import pygame
import sys
import time

# Inicializar pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 600, 650
ROWS, COLS = 8, 8
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

# Colors
WHITE = (245, 255, 245)
GRAY = (144, 238, 144)
DARK_GRAY = (34, 139, 34)
BLACK = (0, 100, 0)

# Fuente
font = pygame.font.SysFont("Arial", 30)

# Data del Juego 
score = 0
start_time = time.time()
elapsed_time = 0


# Usuario desde el Gestion del Usuario
def get_user():
    try:
        with open("user.txt", "r") as f:
            return f.read().strip()
    except:
        return "Guest"


player_name = get_user()


def draw_ui():
    # Barra superior
    ui_rect = pygame.Rect(0, 0, WIDTH, 50)
    new_func(ui_rect)

    # Textos
    name_text = font.render(f"Jugador: {player_name}", True, WHITE)
    time_text = font.render(f"Tiempo: {elapsed_time}s", True, WHITE)
    score_text = font.render(f"Puntos: {score}", True, WHITE)

    # Posiciones
    screen.blit(name_text, (10, 10))
    screen.blit(time_text, (260, 10))
    screen.blit(score_text, (420, 10))

def new_func(ui_rect):
    pygame.draw.rect(screen, DARK_GRAY, ui_rect)


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + 50  # espacio para la barra

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

    # Actualiaz el Tiempo
    elapsed_time = int(time.time() - start_time)

    draw_ui()
    draw_grid()

    pygame.display.update()

pygame.quit()
sys.exit()
