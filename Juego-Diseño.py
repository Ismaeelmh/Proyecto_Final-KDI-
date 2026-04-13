import pygame
import sys
import time

# Inicializar pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 680, 700
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
font = pygame.font.SysFont("Arial", 25)
button_font = pygame.font.SysFont("Arial", 25)
result_font = pygame.font.SysFont("Arial", 30)

# Botones
reinciar_botton = pygame.Rect(520, 12, 110, 35)
salir_botton = pygame.Rect(610, 12, 90, 35)

# Data del Juego
score = 0
start_time = time.time()
elapsed_time = 0

# Resultado
result_text_value = "Resultado: -"

# Usuario desde login
def get_user():
    try:
        with open("user.txt", "r") as f:
            return f.read().strip()
    except:
        return "Guest"

player_name = get_user()


def draw_ui():
    ui_rect = pygame.Rect(0, 0, WIDTH, 50)
    pygame.draw.rect(screen, DARK_GRAY, ui_rect)

    name_text = font.render(f"Jugador: {player_name}", True, WHITE)
    time_text = font.render(f"Tiempo: {elapsed_time}s", True, WHITE)
    score_text = font.render(f"Puntos: {score}", True, WHITE)

    pygame.draw.rect(screen, BLACK, reinciar_botton)
    pygame.draw.rect(screen, BLACK, salir_botton)

    reinciar_text = button_font.render("Reiniciar", True, WHITE)
    salir_text = button_font.render("Salir", True, WHITE)

    screen.blit(reinciar_text, (reinciar_botton.x + 5, reinciar_botton.y + 5))
    screen.blit(salir_text, (salir_botton.x + 15, salir_botton.y + 5))

    screen.blit(name_text, (6, 10))
    screen.blit(time_text, (253, 10))
    screen.blit(score_text, (398, 10))


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + 50

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)


# ✅ Dibujar resultado abajo
def draw_result_text():
    text = result_font.render(result_text_value, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(text, text_rect)


# Reiniciar juego
def reset_game():
    global score, start_time, result_text_value
    score = 0
    start_time = time.time()
    result_text_value = "Resultado: Reiniciado"


# Bucle principal
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

    # Tiempo
    elapsed_time = int(time.time() - start_time)

    draw_ui()
    draw_grid()
    draw_result_text()  # 👈 aquí se dibuja el resultado

    pygame.display.update()

pygame.quit()
sys.exit()
