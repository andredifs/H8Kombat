import sys
import pygame

# Importing constants
from constants import window
from constants import events

# Screens
from include.screens.menu_screen import MenuScreen
from include.screens.choice_screen import ChoiceScreen
from include.screens.fight_screen import FightScreen

pygame.init()

# Windows
WIN = pygame.display.set_mode((window.WIDTH, window.HEIGHT))
pygame.display.set_caption(window.TITLE)

# Main function
def main(dev=False):
    """
    Main game loop.

    Handles events, draws the current screen, and updates the game state.

    Args:
        dev (bool): Optional parameter, default False. If True, runs the game in developer mode.

    Returns:
        None
    """
    global WIN
    menu_screen = MenuScreen(WIN)
    choice_screen = ChoiceScreen(WIN)
    current_screen = menu_screen

    if dev:
        current_screen = FightScreen(dev=True, WIN=WIN)

    while True:
        current_screen.draw()
        current_screen.update()
        current_screen.handle_events()

        for event in pygame.event.get():
            if event.type == events.CHOICE:
                current_screen = choice_screen
            elif event.type == events.FIGHT:
                pygame.display.set_caption("Fight!")
                current_screen = FightScreen(WIN, characters=event.characters)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
