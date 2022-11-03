import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 600))

circle(screen, (255, 255, 0), (300, 300), 250)
circle(screen, (255, 0, 0), (200, 230), 50)
circle(screen, (255, 0, 0), (400, 230), 50)
circle(screen, (0, 0, 0), (200, 230), 25)
circle(screen, (0, 0, 0), (400, 230), 25)
rect(screen, (0, 0, 0), (150, 400, 300, 20))
pygame.draw.polygon(screen, (139, 69, 19),
                    [[50, 20], [260, 160],
                     [260, 190], [50, 50]])
pygame.draw.polygon(screen, (139, 69, 19),
                    [[550, 20], [350, 160],
                     [350, 190], [550, 50]])

pygame.display.update()
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()