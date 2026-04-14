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
        