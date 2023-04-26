# transform in class
# def health_bar(health, x, y):
#     ratio = health / 100
#     pygame.draw.rect(WIN_GAME, colors.BLACK, (x - 2, y - 2, 204, 34))
#     pygame.draw.rect(WIN_GAME, colors.GREY, (x, y, 200, 30))

#     if health > 40:
#         color = colors.GREEN
#     elif health > 20:
#         color = colors.YELLOW
#     else:
#         color = colors.RED

#     pygame.draw.rect(WIN_GAME, color, (x, y, 200 * ratio, 30))

import pygame
from constants import colors

class HealthBar():
    def __init__(self, health: int, x: int, y: int, surface: pygame.Surface):
        self.health = health
        self.x = x
        self.y = y
        self.surface = surface

    def update(self, health):
        self.health = health
        self.draw()

    def draw(self):
        ratio = self.health / 100
        pygame.draw.rect(self.surface, colors.BLACK, (self.x - 2, self.y - 2, 204, 34))
        pygame.draw.rect(self.surface, colors.GREY, (self.x, self.y, 200, 30))

        if self.health > 40:
            color = colors.GREEN
        elif self.health > 20:
            color = colors.YELLOW
        else:
            color = colors.RED

        pygame.draw.rect(self.surface, color, (self.x, self.y, 200 * ratio, 30))
