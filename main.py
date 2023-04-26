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

# Backgrounds
PICTURE_MENU = pygame.image.load("assets/menu.png")
BG_MENU = pygame.transform.scale(PICTURE_MENU, (window.WIDTH, window.HEIGHT))

PICTURE_GAME = pygame.image.load("assets/tatame.jpg")
BG_GAME = pygame.transform.scale(PICTURE_GAME, (window.WIDTH, window.HEIGHT))

PICTURE_VICTORY = pygame.image.load("assets/fatality.jpg")
BG_VICTORY = pygame.transform.scale(PICTURE_VICTORY, (window.WIDTH, window.HEIGHT))

class MenuScreen():
    # Botões
    PLAY_BUTTON = menu_button(text_input="PLAY", pos=(window.WIDTH / 2, window.HEIGHT / 2))
    OPTIONS_BUTTON = menu_button(text_input="OPTIONS", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 80))
    QUIT_BUTTON = menu_button(text_input="QUIT", pos=(window.WIDTH / 2, window.HEIGHT / 2 + 160))

    # Posição do mouse
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    def handle_events(self):
        # Verifica se o botão foi clicado
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
        WIN.blit(BG_MENU, (0, 0))

        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = utils.get_font(100).render("H8 Kombat", True, colors.WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(window.WIDTH / 2, window.HEIGHT / 4))

        WIN.blit(MENU_TEXT, MENU_RECT)

        # Muda a cor do botão quando o mouse está em cima
        for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
            button.changeColor(self.MENU_MOUSE_POS)
            button.update(WIN)

        pygame.display.update()

    def draw(self):
        pass

class FightScreen():
    TEXT_SURFACE = WIN.subsurface(pygame.Rect(0, 0, window.WIDTH, window.HEIGHT))
    round_over = False
    round_over_time = pygame.time.get_ticks()
    intro_count = 3

    # Create a two fighters for game
    fighter_1 = Fighter(100, 310, WIN, colors.BLUE)
    fighter_2 = Fighter(800 - 180, 310, WIN, colors.ORANGE)

    bar_1 = HealthBar(fighter_1.health, 20, 20, WIN)
    bar_2 = HealthBar(fighter_2.health, 580, 20, WIN)

    # Defining oponent
    fighter_1.set_target(fighter_2)
    fighter_2.set_target(fighter_1)

    # Defining controls
    fighter_1.set_controls(controls.PLAYER1)
    fighter_2.set_controls(controls.PLAYER2)

    def handle_events(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()

    def update(self):
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
        self.fighter_1.reset()
        self.fighter_2.reset()


menu_screen = MenuScreen()
fight_screen = FightScreen()
current_screen = menu_screen

# Main function
def main(dev=False):
    while True:
        current_screen.handle_events()
        current_screen.draw()
        current_screen.update()
