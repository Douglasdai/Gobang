import pygame
import time
import random
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
pygame.init()
game_font = pygame.font.SysFont('SimHei', 24)
game_clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_starttime = time.time()