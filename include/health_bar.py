import pygame
from constants import colors

class HealthBar():
    """
    A class representing a health bar.

    ...

    Attributes
    ----------
    health : int
        The initial health of the entity.
    x : int
        The x-coordinate of the health bar on the screen.
    y : int
        The y-coordinate of the health bar on the screen.
    surface : pygame.Surface
        The surface on which the health bar will be drawn.

    Methods
    -------
    update(health: int) -> None:
        Updates the current health of the entity and draws the health bar on the surface.
    draw() -> None:
        Draws the health bar on the surface.
    """

    def __init__(self, health: int, x: int, y: int, surface: pygame.Surface):
        """
        Constructs all the necessary attributes for the HealthBar object.

        Parameters
        ----------
        health : int
            The initial health of the entity.
        x : int
            The x-coordinate of the health bar on the screen.
        y : int
            The y-coordinate of the health bar on the screen.
        surface : pygame.Surface
            The surface on which the health bar will be drawn.
        """
        self.health = health
        self.x = x
        self.y = y
        self.surface = surface

    def update(self, health):
        """
        Updates the current health of the entity and draws the health bar on the surface.

        Parameters
        ----------
        health : int
            The updated health of the entity.
        """
        self.health = health
        self.draw()

    def draw(self):
        """
        Draws the health bar on the surface.
        """
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
