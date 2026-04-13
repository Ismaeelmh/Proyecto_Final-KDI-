import pygame
import sys
import time

pygame.init()

# Configuración
WIDTH = 680
ROWS, COLS = 8, 8

TOP_BAR = 50
BOTTOM_BAR = 50

CELL_SIZE = WIDTH // COLS
HEIGHT = TOP_BAR + (CELL_SIZE * ROWS) + BOTTOM_BAR

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

# Colors
WHITE = (245, 255, 245)
GRAY = (144, 238, 144)
DARK_GRAY = (34, 139, 34)
BLACK = (0, 100, 0)

# Fuentes
font = pygame.font.SysFont("Arial", 25)
button_font = pygame.font.SysFont("Arial", 25)
result_font = pygame.font.SysFont("Arial", 28)

# Botones
reinciar_botton = pygame.Rect(520, 12, 110, 35)
salir_botton = pygame.Rect(610, 12, 90, 35)

# Data
score = 0
start_time = time.time()
elapsed_time = 0

result_text_value = "Resultado:"

def get_user():
    try:
        with open("user.txt", "r") as f:
            return f.read().strip()
    except:
        return "Guest"

player_name = get_user()


def draw_ui():
    # Top bar
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, TOP_BAR))

    name_text = font.render(f"Jugador: {player_name}", True, WHITE)
    time_text = font.render(f"Tiempo: {elapsed_time}s", True, WHITE)
    score_text = font.render(f"Puntos: {score}", True, WHITE)

    pygame.draw.rect(screen, BLACK, reinciar_botton)
    pygame.draw.rect(screen, BLACK, salir_botton)

    screen.blit(button_font.render("Reiniciar", True, WHITE), (525, 15))
    screen.blit(button_font.render("Salir", True, WHITE), (625, 15))

    screen.blit(name_text, (6, 10))
    screen.blit(time_text, (250, 10))
    screen.blit(score_text, (400, 10))

    # Bottom bar
    pygame.draw.rect(screen, DARK_GRAY, (0, HEIGHT - BOTTOM_BAR, WIDTH, BOTTOM_BAR))

    result_text = result_font.render(result_text_value, True, WHITE)
    rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
    screen.blit(result_text, rect)


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + TOP_BAR

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)


def reset_game():
    global score, start_time, result_text_value
    score = 0
    start_time = time.time()
    result_text_value = "Resultado: Reiniciado"


running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if reinciar_botton.collidepoint(mouse_pos):
                reset_game()

            if salir_botton.collidepoint(mouse_pos):
                running = False

    elapsed_time = int(time.time() - start_time)

    draw_ui()
    draw_grid()

    pygame.display.update()

pygame.quit()
sys.exit()
