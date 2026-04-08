import pygame
import sys

# Inicializar pygame
pygame.init()

# Tamaño de la ventana
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("Sistema de Sesiones")

# Colores
Blanco = (255, 255, 255)
Negro = (0, 0, 0)
Gris = (128, 128, 128)
Verde = (0, 255, 0)
Rojo = (255, 0, 0)

# Fuente
Font = pygame.font.SysFont(None, 40)

# Variables de entrada
input_user = ""
input_pass = ""
active_user = False
active_pass = False

# Credenciales
CORRECT_USER= "buscaminas"
CORRECT_PASS = "buscaminas123"

# Estado
login_success = False
message = ""

# Variable para mantener sesión activa
session_active = False 

## Botón de logout
logout_rect = pygame.Rect(600, 550, 200, 50)

running = True
while running:
    screen.fill(Blanco)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Click del ratón
        if event.type == pygame.MOUSEBUTTONDOWN:

            ## Detectar click en logout
            if session_active and logout_rect.collidepoint(event.pos):
                session_active = False
                login_success = False
                input_user = ""
                input_pass = ""
                message = "Sesión cerrada"

            elif 500 <= event.pos[0] <= 900 and 250 <= event.pos[1] <= 300:
                active_user = True
                active_pass = False
            elif 500 <= event.pos[0] <= 900 and 350 <= event.pos[1] <= 400:
                active_pass = True
                active_user = False
            else:
                active_user = False
                active_pass = False

        # Teclado
        if event.type == pygame.KEYDOWN:

            # ENTER primero (login)
            if event.key == pygame.K_RETURN:
                if input_user == CORRECT_USER and input_pass == CORRECT_PASS:
                    login_success = True
                    session_active = True
                    message = "Login correcto"
                else:
                    login_success = False
                    message = "Usuario o contraseña incorrectos"

            # Escribir usuario
            elif active_user:
                if event.key == pygame.K_BACKSPACE:
                    input_user = input_user[:-1]
                else:
                    input_user += event.unicode
                    login_success = False
                    message = ""

            # Escribir contraseña
            elif active_pass:
                if event.key == pygame.K_BACKSPACE:
                    input_pass = input_pass[:-1]
                else:
                    input_pass += event.unicode
                    login_success = False
                    message = ""

    # Mensaje y desactivar cajas si la sesión está activa
    if session_active:
        message = f"¡Bienvenido {CORRECT_USER}!"
        active_user = False
        active_pass = False

    ## Solo permitir inputs si NO hay sesión activa
    if not session_active:
        # Dibujar cajas
        pygame.draw.rect(screen, Gris, (475, 250, 250, 50))
        pygame.draw.rect(screen, Gris, (520, 350, 250, 50))

        # Texto dentro de las cajas
        user_text = Font.render(input_user, True, Negro)
        pass_text = Font.render("*" * len(input_pass), True, Negro)

        screen.blit(user_text, (480, 260))
        screen.blit(pass_text, (522, 360))

        # Etiquetas
        screen.blit(Font.render("Usuario:", True, Negro), (350, 260))
        screen.blit(Font.render("Contraseña:", True, Negro), (350, 360))

    ## Dibujar botón logout cuando sesión activa
    if session_active:
        pygame.draw.rect(screen, Rojo, logout_rect)
        screen.blit(Font.render("Cerrar sesión", True, Blanco), (610, 560))

    # Mensaje
    color_msg = Verde if login_success else Rojo
    screen.blit(Font.render(message, True, color_msg), (500, 450))

    pygame.display.flip()

pygame.quit()
sys.exit()