from asyncio import Event

import pygame
import sys

# Inicializar el pygame
pygame.init()

# Tamaño de la ventana
screen = pygame.display.set_mode((1400,800))
pygame.display.set_caption("Sistema del Sesiones")

#Colors
Blanco = (255,255,255)
Negro = (0,0,0)

# Fuente

Font = pygame.font.SysFont(None, 40)

# Bucle Principal
running = True
while running:
    screen.fill(Blanco)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()