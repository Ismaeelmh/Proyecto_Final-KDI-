import pygame
import sys
import time
import random 

pygame.init()

# Configuración básica
WIDTH = 680
ROWS, COLS = 8, 8

TOP_BAR = 50
BOTTOM_BAR = 50

CELL_SIZE = WIDTH // COLS
HEIGHT = TOP_BAR + (CELL_SIZE * ROWS) + BOTTOM_BAR

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

# Colores
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

# Datos del juego
score = 0
start_time = time.time()
elapsed_time = 0

result_text_value = "Resultado:"

# Estado de celdas
grid_state = [[False for _ in range(COLS)] for _ in range(ROWS)]

# estado de banderas
flag_state = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Tablero con minas (0 = vacío, -1 = mina)
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Colocar minas
def place_mines(num_mines=10):
    placed = 0
    while placed < num_mines:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)

        if board[r][c] != -1:
            board[r][c] = -1
            placed += 1

# Calcular números
def calculate_numbers():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == -1:
                continue

            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    r = row + dr
                    c = col + dc

                    if 0 <= r < ROWS and 0 <= c < COLS:
                        if board[r][c] == -1:
                            count += 1

            board[row][col] = count

# Inicializar tablero
place_mines()
calculate_numbers()

# Usuario
def get_user():
    try:
        with open("user.txt", "r") as f:
            return f.read().strip()
    except:
        return "Guest"

player_name = get_user()


# UI
def draw_ui():
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

    pygame.draw.rect(screen, DARK_GRAY, (0, HEIGHT - BOTTOM_BAR, WIDTH, BOTTOM_BAR))

    result_text = result_font.render(result_text_value, True, WHITE)
    rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
    screen.blit(result_text, rect)


# Grid
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + TOP_BAR

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if grid_state[row][col]:
                pygame.draw.rect(screen, GRAY, rect)

                # Mostrar mina o número
                if board[row][col] == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, 10)
                elif board[row][col] > 0:
                    text = font.render(str(board[row][col]), True, BLACK)
                    screen.blit(text, (x + 30, y + 20))
            else:
                pygame.draw.rect(screen, WHITE, rect)

            pygame.draw.rect(screen, BLACK, rect, 2)

            # dibujar bandera
            if flag_state[row][col]:
                pygame.draw.circle(screen, BLACK, rect.center, 8)


# Reiniciar
def reset_game():
    global score, start_time, result_text_value, grid_state, flag_state, board  

    score = 0
    start_time = time.time()
    result_text_value = "Resultado:"

    grid_state = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flag_state = [[False for _ in range(COLS)] for _ in range(ROWS)]

    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    place_mines()
    calculate_numbers()


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

            # CLIC IZQUIERDO
            if event.button == 1:
                mouse_x, mouse_y = mouse_pos

                if TOP_BAR <= mouse_y <= HEIGHT - BOTTOM_BAR:
                    col = mouse_x // CELL_SIZE
                    row = (mouse_y - TOP_BAR) // CELL_SIZE

                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if not flag_state[row][col]:
                            grid_state[row][col] = True
                            result_text_value = f"Celda ({row},{col}) descubierta"

            # CLIC DERECHO (banderas)
            if event.button == 3:
                mouse_x, mouse_y = mouse_pos

                if TOP_BAR <= mouse_y <= HEIGHT - BOTTOM_BAR:
                    col = mouse_x // CELL_SIZE
                    row = (mouse_y - TOP_BAR) // CELL_SIZE

                    if 0 <= row < ROWS and 0 <= col < COLS:
                        flag_state[row][col] = not flag_state[row][col]
                        result_text_value = f"Bandera en ({row},{col})"

    elapsed_time = int(time.time() - start_time)

    draw_ui()
    draw_grid()

    pygame.display.update()

pygame.quit()
sys.exit()
