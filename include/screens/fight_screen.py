import sys
import pygame
import utils

from constants import window
from constants import colors
from constants import controls
from constants import fight as fight_constants
from constants.characters import fighters

from include.fighter import Fighter
from include.health_bar import HealthBar

PICTURE_GAME = pygame.image.load("assets/tatame.jpg")
BG_GAME = pygame.transform.scale(PICTURE_GAME, (window.WIDTH, window.HEIGHT))

PICTURE_VICTORY = pygame.image.load("assets/fatality.jpg")
BG_VICTORY = pygame.transform.scale(PICTURE_VICTORY, (window.WIDTH, window.HEIGHT))


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

    def __init__(self, WIN, characters=[], dev=False):
        self.WIN = WIN
        self.TEXT_SURFACE = WIN.subsurface(pygame.Rect(0, 0, window.WIDTH, window.HEIGHT))
        self.round_over = False
        self.round_over_time = pygame.time.get_ticks()
        self.intro_count = 3

        if dev:
            # Create a two fighters for game
            self.fighter_1 = Fighter(100, 310, self.WIN, fighters.get("anao"))
            self.fighter_2 = Fighter(800 - 180, 310, self.WIN, fighters.get("lula"))

        else:
            self.fighter_1 = Fighter(100, 310, self.WIN, fighters.get(characters[0]))
            self.fighter_2 = Fighter(800 - 180, 310, self.WIN, fighters.get(characters[1]))

        self.setup()

    def setup(self):
        self.bar_1 = HealthBar(self.fighter_1.health, 20, 20, self.WIN)
        self.bar_2 = HealthBar(self.fighter_2.health, 580, 20, self.WIN)

        # Defining oponent
        self.fighter_1.set_target(self.fighter_2)
        self.fighter_2.set_target(self.fighter_1)

        # Defining controls
        self.fighter_1.set_controls(controls.PLAYER1)
        self.fighter_2.set_controls(controls.PLAYER2)

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

            utils.draw_text(self.WIN, text, 100, colors.RED, window.WIDTH / 2, window.HEIGHT / 2)
            pygame.display.update()
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
            self.WIN.blit(BG_VICTORY, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

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
        self.WIN.blit(BG_GAME, (0, 0))

        # Draw fighters
        self.fighter_1.draw()
        self.fighter_2.draw()

        # Draw health bars
        self.bar_1.draw()
        self.bar_2.draw()

        utils.draw_text(self.WIN, f'P1: {self.fighter_1.score}', 30, colors.RED, 55, 70)
        utils.draw_text(self.WIN, f'P2: {self.fighter_2.score}', 30, colors.RED, window.WIDTH - 55, 70)

        # display victory image
        if (self.fighter_1.score == 2) or (self.fighter_2.score == 2):
            self.WIN.blit(BG_VICTORY, (0, 0))

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
