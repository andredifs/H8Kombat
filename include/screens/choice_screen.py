import sys
import pygame
from include.button import choice_button, menu_button
import utils

from constants import window
from constants import colors
from constants import events

PICTURE_MENU = pygame.image.load("assets/menu.png")
BG_MENU = pygame.transform.scale(PICTURE_MENU, (window.WIDTH, window.HEIGHT))

ANAO_IMG = pygame.image.load("assets/anao.png")
LULA_IMG = pygame.image.load("assets/lula.png")
QUINZE_IMG = pygame.image.load("assets/15.png")

class ChoiceScreen():
    def __init__(self, WIN):
        self.WIN = WIN
        self.selected_caracters = []

        # Buttons
        self.PLAY_BUTTON = menu_button(text_input="PLAY", pos=(window.WIDTH / 2, window.HEIGHT / 2))

        # Choices buttons
        self.ANAO_BUTTON = choice_button(ANAO_IMG, (150, 150), text_input="", pos=(
            window.WIDTH / 2 - 200, window.HEIGHT / 2 + 150), selected="anao" in self.selected_caracters)

        self.LULA_BUTTON = choice_button(LULA_IMG, (150, 150), text_input="", pos=(
            window.WIDTH / 2, window.HEIGHT / 2 + 150), selected="lula" in self.selected_caracters)

        self.QUINZE_BUTTON = choice_button(QUINZE_IMG, (150, 150), text_input="", pos=(
            window.WIDTH / 2 + 200, window.HEIGHT / 2 + 150), selected="quinze" in self.selected_caracters)

        # Mouse position
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

    def handle_events(self):
        """
        Handles the events in the main menu screen, such as mouse clicks and the window closing.
        """
        # Check if button was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    global current_screen
                    current_screen = pygame.event.post(pygame.event.Event(events.FIGHT, action="fight", characters=self.selected_caracters))
                    print("Play game")
                if self.ANAO_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    print("Anão")
                    if "anao" in self.selected_caracters:
                        self.selected_caracters.remove("anao")
                        self.ANAO_BUTTON.selected = False
                    else:
                        self.selected_caracters.append("anao")
                        self.ANAO_BUTTON.selected = True
                if self.LULA_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    print("Lula")
                    if "lula" in self.selected_caracters:
                        self.selected_caracters.remove("lula")
                        self.LULA_BUTTON.selected = False
                    else:
                        self.selected_caracters.append("lula")
                        self.LULA_BUTTON.selected = True
                if self.QUINZE_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    print("15")
                    if "quinze" in self.selected_caracters:
                        self.selected_caracters.remove("quinze")
                        self.QUINZE_BUTTON.selected = False
                    else:
                        self.selected_caracters.append("quinze")
                        self.QUINZE_BUTTON.selected = True

    def update(self):
        """
        Updates the menu screen with the latest changes, such as button colors and positions.

        :return: None
        """
        self.WIN.blit(BG_MENU, (0, 0))

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = utils.get_font(100).render("Select Fighters", True, colors.WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(window.WIDTH / 2, window.HEIGHT / 8))

        self.WIN.blit(MENU_TEXT, MENU_RECT)

        # Changes the color of each button if the mouse is hovering over it, then updates its position.
        for button in [self.PLAY_BUTTON, self.ANAO_BUTTON, self.LULA_BUTTON, self.QUINZE_BUTTON]:
            button.changeColor(self.MENU_MOUSE_POS)
            button.update(self.WIN)

        pygame.display.update()

    def draw(self):
        """
        Draws the menu screen with its current settings.

        :return: None
        """
        pass
