import pygame

# Importing constants
from constants import window
from constants import colors
from constants import controls
from constants import fight as fight_constants

# Importing utils
import utils

# Include classes
from include.button import menu_button
from include.fighter import Fighter
from include.health_bar import HealthBar

pygame.init()

# Windows
WIN = pygame.display.set_mode((window.WIDTH, window.HEIGHT))
pygame.display.set_caption(window.TITLE)

# Set the game clock
FPS = 60

# Load sprites
anao_sheets = [
    pygame.image.load("assets/sprites/anao_movimento.png").convert_alpha(),
    pygame.image.load("assets/sprites/anao_soco.png").convert_alpha(),
    pygame.image.load("assets/sprites/anao_chute.png").convert_alpha(),
]

lula_sheets = [
    pygame.image.load("assets/sprites/lula_movimento.png").convert_alpha(),
    pygame.image.load("assets/sprites/lula_soco.png").convert_alpha(),
    pygame.image.load("assets/sprites/lula_chute.png").convert_alpha(),
]

# Backgrounds
PICTURE_MENU = pygame.image.load("assets/menu.png")
BG_MENU = pygame.transform.scale(PICTURE_MENU, (window.WIDTH, window.HEIGHT))

PICTURE_GAME = pygame.image.load("assets/tatame.jpg")
BG_GAME = pygame.transform.scale(PICTURE_GAME, (window.WIDTH, window.HEIGHT))

PICTURE_VICTORY = pygame.image.load("assets/fatality.jpg")
BG_VICTORY = pygame.transform.scale(PICTURE_VICTORY, (window.WIDTH, window.HEIGHT))


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
    # Buttons
    PLAY_BUTTON = menu_button(text_input="PLAY", pos=(window.WIDTH / 2, window.HEIGHT / 2))
    OPTIONS_BUTTON = menu_button(text_input="OPTIONS", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 80))
    QUIT_BUTTON = menu_button(text_input="QUIT", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 160))

    # Mouse position
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    def handle_events(self):
        """
        Handles the events in the main menu screen, such as mouse clicks and the window closing.
        """
        # Check if button was clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    global current_screen
                    current_screen = fight_screen
                    print("Play game")
                if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    print("Open options")
                if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    pygame.quit()

    def update(self):
        """
        Updates the menu screen with the latest changes, such as button colors and positions.

        :return: None
        """
        WIN.blit(BG_MENU, (0, 0))

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = utils.get_font(100).render("H8 Kombat", True, colors.WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(window.WIDTH / 2, window.HEIGHT / 4))

        WIN.blit(MENU_TEXT, MENU_RECT)

        # Changes the color of each button if the mouse is hovering over it, then updates its position.
        for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
            button.changeColor(self.MENU_MOUSE_POS)
            button.update(WIN)

        pygame.display.update()

    def draw(self):
        """
        Draws the menu screen with its current settings.

        :return: None
        """
        pass


class FightScreen():
    """
    A class representing the main game screen.

    ...

    Attributes
    ----------
    TEXT_SURFACE : pygame.Surface
        A surface that represents the area where the text is displayed.
    round_over : bool
        A boolean that indicates if the round is over.
    round_over_time : int
        The time in milliseconds that the round has been over.
    intro_count : int
        An integer that counts down from 3 to 0 before the fight begins.
    fighter_1 : Fighter
        A Fighter object representing the first fighter in the game.
    fighter_2 : Fighter
        A Fighter object representing the second fighter in the game.
    bar_1 : HealthBar
        A HealthBar object representing the health bar of the first fighter.
    bar_2 : HealthBar
        A HealthBar object representing the health bar of the second fighter.

    Methods
    -------
    handle_events():
        Handles events that occur in the game, such as quitting.
    update():
        Updates the game screen, including the fighters' movements and health bars,
        the countdown before the fight, and the victory image.
    """

    TEXT_SURFACE = WIN.subsurface(pygame.Rect(0, 0, window.WIDTH, window.HEIGHT))
    round_over = False
    round_over_time = pygame.time.get_ticks()
    intro_count = 3

    # Create a two fighters for game
    fighter_1 = Fighter(100, 310, WIN, anao_sheets)
    fighter_2 = Fighter(800 - 180, 310, WIN, lula_sheets)

    bar_1 = HealthBar(fighter_1.health, 20, 20, WIN)
    bar_2 = HealthBar(fighter_2.health, 580, 20, WIN)

    # Defining oponent
    fighter_1.set_target(fighter_2)
    fighter_2.set_target(fighter_1)

    # Defining controls
    fighter_1.set_controls(controls.PLAYER1)
    fighter_2.set_controls(controls.PLAYER2)

    def handle_events(self):
        """
        Handles events that occur in the game, such as quitting.
        """
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()

    def update(self):
        """
        Update the state of the FightScreen.

        This method updates the player's health bars, countdown timer,
        players' position, checks for player defeat and displays victory image if
        either player has a score of 2.

        Args:
            None

        Returns:
            None
        """
        # Player stats
        self.bar_1.update(self.fighter_1.health)
        self.bar_2.update(self.fighter_2.health)

        # update countdown
        if self.intro_count >= 0:
            text = str(self.intro_count) if self.intro_count > 0 else "FIGHT!"

            utils.draw_text(WIN, text, 100, colors.RED, window.WIDTH / 2, window.HEIGHT / 2)

            pygame.time.delay(1000)
            self.intro_count -= 1

        elif self.round_over is False:
            self.fighter_1.move(window.WIDTH, window.HEIGHT)
            self.fighter_2.move(window.WIDTH, window.HEIGHT)
            self.fighter_1.update()
            self.fighter_2.update()

        # check for player defeat
        if self.round_over is False:
            if self.fighter_1.dead or self.fighter_2.dead:
                alive = self.fighter_1 if not self.fighter_1.dead else self.fighter_2
                alive.score += 1
                self.round_over = True
                self.round_over_time = pygame.time.get_ticks()

                self.reset_fighters()

        elif pygame.time.get_ticks() - self.round_over_time > fight_constants.ROUND_OVER_COOLDOWN:
            self.round_over = False
            self.intro_count = 3
            self.reset_fighters()

        # display victory image
        if (self.fighter_1.score == 2) or (self.fighter_2.score == 2):
            WIN.blit(BG_VICTORY, (0, 0))

        pygame.display.update()

    def draw(self):
        """
        Draw the game screen.

        Draws the background image, fighters, health bars and player scores. If either fighter has reached 2 points,
        it also displays a victory image.

        Args:
            None

        Returns:
            None
        """
        WIN.blit(BG_GAME, (0, 0))

        # Draw fighters
        self.fighter_1.draw()
        self.fighter_2.draw()

        # Draw health bars
        self.bar_1.draw()
        self.bar_2.draw()

        utils.draw_text(WIN, f'P1: {self.fighter_1.score}', 30, colors.RED, 55, 70)
        utils.draw_text(WIN, f'P2: {self.fighter_2.score}', 30, colors.RED, window.WIDTH - 55, 70)

        # display victory image
        if (self.fighter_1.score == 2) or (self.fighter_2.score == 2):
            WIN.blit(BG_VICTORY, (0, 0))

    def reset_fighters(self):
        """
        Reset both fighters to their initial state.

        Args:
            None

        Returns:
            None
        """
        self.fighter_1.reset()
        self.fighter_2.reset()


menu_screen = MenuScreen()
fight_screen = FightScreen()
current_screen = menu_screen

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
    if dev:
        global current_screen
        current_screen = fight_screen

    while True:
        current_screen.handle_events()
        current_screen.draw()
        current_screen.update()
