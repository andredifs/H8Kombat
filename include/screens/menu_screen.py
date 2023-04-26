import sys
import pygame
from include.button import menu_button
import utils

from constants import window
from constants import colors
from constants import events

PICTURE_MENU = pygame.image.load("assets/menu.png")
BG_MENU = pygame.transform.scale(PICTURE_MENU, (window.WIDTH, window.HEIGHT))

class MenuScreen():
    """
    A class representing the main menu screen.

    Attributes:
    -----------
    PLAY_BUTTON : object
        A menu button object to start the game.
    OPTIONS_BUTTON : object
        A menu button object to open the options screen.
    QUIT_BUTTON : object
        A menu button object to quit the game.
    MENU_MOUSE_POS : tuple
        A tuple with the x and y positions of the mouse in the menu screen.

    Methods:
    --------
    handle_events(self):
        Handles the events in the main menu screen, such as mouse clicks and the window closing.

    update(self):
        Updates the graphics and buttons on the main menu screen.

    draw(self):
        Draws the main menu screen.
    """

    def __init__(self, WIN):
        self.WIN = WIN
        # Buttons
        self.PLAY_BUTTON = menu_button(text_input="PLAY", pos=(window.WIDTH / 2, window.HEIGHT / 2))
        self.OPTIONS_BUTTON = menu_button(text_input="OPTIONS", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 80))
        self.QUIT_BUTTON = menu_button(text_input="QUIT", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 160))

        # Mouse position
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

    def handle_events(self):
        """
        Handles the events in the main menu screen, such as mouse clicks and the window closing.
        """
        # Check if button was clicked
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    pygame.event.post(pygame.event.Event(events.CHOICE, action="choice"))
                    print("Play game")
                if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    print("Open options")
                if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

    def update(self):
        """
        Updates the menu screen with the latest changes, such as button colors and positions.

        :return: None
        """
        self.WIN.blit(BG_MENU, (0, 0))

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = utils.get_font(100).render("H8 Kombat", True, colors.WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(window.WIDTH / 2, window.HEIGHT / 4))

        self.WIN.blit(MENU_TEXT, MENU_RECT)

        # Changes the color of each button if the mouse is hovering over it, then updates its position.
        for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
            button.changeColor(self.MENU_MOUSE_POS)
            button.update(self.WIN)

        pygame.display.update()

    def draw(self):
        """
        Draws the menu screen with its current settings.

        :return: None
        """
        pass
