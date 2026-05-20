import pygame
import time
import random
import asyncio
import requests


pygame.init()



session_requests = requests.Session()
response = requests.get("http://127.0.0.1:5000/usuario")

print("STATUS:", response.status_code)
print("TEXT:", response.text)

if response.status_code != 200:
    print("Error: no login o sesión perdida")
    exit()

try:
    data = response.json()
except:
    print("Respuesta no es JSON válido")
    exit()
usuario_id = data["usuario_id"]
player_name = data["nombre"]



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
HIGHLIGHT = (0, 160, 0)

# Fuentes
font = pygame.font.SysFont("Arial", 25)
button_font = pygame.font.SysFont("Arial", 25)
result_font = pygame.font.SysFont("Arial", 28)

# Botones
reinciar_botton = pygame.Rect(470, 12, 110, 35)
salir_botton = pygame.Rect(590, 12, 90, 35)

# Datos del juego
score = 0
start_time = time.time()
elapsed_time = 0
final_time = None

result_text_value = "Resultado:"
game_over = False

# Estado de celdas
grid_state = [[False for _ in range(COLS)] for _ in range(ROWS)]
flag_state = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Tablero
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def place_mines(num_mines=10):
    placed = 0
    while placed < num_mines:
        r = random.randint(0, ROWS - 1)
        c = random.randint(0, COLS - 1)

        if board[r][c] != -1:
            board[r][c] = -1
            placed += 1

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

place_mines()
calculate_numbers()

def reveal_empty(row, col):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return

    if grid_state[row][col] or flag_state[row][col]:
        return

    grid_state[row][col] = True

    if board[row][col] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    reveal_empty(row + dr, col + dc)

def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != -1 and not grid_state[r][c]:
                return False
    return True


def draw_ui():
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, TOP_BAR))

    name_text = font.render(player_name, True, WHITE)
    time_text = font.render(f"Tiempo: {elapsed_time}s", True, WHITE)
    score_text = font.render(f"Puntos: {score}", True, WHITE)

    screen.blit(name_text, (6, 10))
    screen.blit(time_text, (200, 10))
    screen.blit(score_text, (330, 10))

    pygame.draw.rect(screen, DARK_GRAY, (0, HEIGHT - BOTTOM_BAR, WIDTH, BOTTOM_BAR))

    result_text = result_font.render(result_text_value, True, WHITE)
    rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
    screen.blit(result_text, rect)

    if game_over and result_text_value == "¡Perdiste!":
        pygame.draw.rect(screen, HIGHLIGHT, reinciar_botton, border_radius=6)
        pygame.draw.rect(screen, HIGHLIGHT, salir_botton, border_radius=6)

        pygame.draw.rect(screen, BLACK, reinciar_botton, 2, border_radius=6)
        pygame.draw.rect(screen, BLACK, salir_botton, 2, border_radius=6)

        screen.blit(button_font.render("Reiniciar", True, WHITE), (478, 15))
        screen.blit(button_font.render("Salir", True, WHITE), (605, 15))


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + TOP_BAR

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if grid_state[row][col]:
                pygame.draw.rect(screen, GRAY, rect)

                if board[row][col] == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, 10)
                elif board[row][col] > 0:
                    text = font.render(str(board[row][col]), True, BLACK)
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, WHITE, rect)

            pygame.draw.rect(screen, BLACK, rect, 2)

            if flag_state[row][col]:
                pygame.draw.circle(screen, BLACK, rect.center, 8)


def reset_game():
    global score, start_time, result_text_value, grid_state, flag_state, board, game_over, final_time

    score = 0
    start_time = time.time()
    final_time = None
    result_text_value = "Resultado:"
    game_over = False

    grid_state = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flag_state = [[False for _ in range(COLS)] for _ in range(ROWS)]
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    place_mines()
    calculate_numbers()


async def main():
    global elapsed_time, result_text_value, game_over, score, final_time

    running = True

    while running:
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if game_over and result_text_value == "¡Perdiste!":
                    if reinciar_botton.collidepoint(mouse_pos):
                        reset_game()

                    if salir_botton.collidepoint(mouse_pos):
                        running = False

                if not game_over:

                    if event.button == 1:
                        mouse_x, mouse_y = mouse_pos

                        if TOP_BAR <= mouse_y <= HEIGHT - BOTTOM_BAR:
                            col = mouse_x // CELL_SIZE
                            row = (mouse_y - TOP_BAR) // CELL_SIZE

                            if 0 <= row < ROWS and 0 <= col < COLS:
                                if not flag_state[row][col]:

                                    if board[row][col] == -1:
                                        result_text_value = "¡Perdiste!"
                                        game_over = True
                                        final_time = elapsed_time

                                        for r in range(ROWS):
                                            for c in range(COLS):
                                                if board[r][c] == -1:
                                                    grid_state[r][c] = True

                                    elif board[row][col] == 0:
                                        grid_state[row][col] = True
                                        reveal_empty(row, col)
                                        score += 1
                                    else:
                                        grid_state[row][col] = True
                                        score += 1

                    if event.button == 3:
                        mouse_x, mouse_y = mouse_pos

                        if TOP_BAR <= mouse_y <= HEIGHT - BOTTOM_BAR:
                            col = mouse_x // CELL_SIZE
                            row = (mouse_y - TOP_BAR) // CELL_SIZE

                            if 0 <= row < ROWS and 0 <= col < COLS:
                                if not grid_state[row][col]:
                                    flag_state[row][col] = not flag_state[row][col]

        if not game_over:
            elapsed_time = int(time.time() - start_time)

        if not game_over and check_win():
            result_text_value = "¡Ganaste!"
            game_over = True
            final_time = elapsed_time
            score += 15

        draw_ui()
        draw_grid()

        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())