import pygame
import constants.movement


class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))  # create a rect of fighter
        self.vel_y = 0

    def move(self, screen_width, screen_height):
        dx = 0
        dy = 0

        # get keypress
        key = pygame.key.get_pressed()

        # movement
        if key[pygame.K_a]:
            dx = -constants.movement.SPEED_X
        if key[pygame.K_d]:
            dx = constants.movement.SPEED_X

        # jump
        if key[pygame.K_w]:
            self.vel_y = - constants.movement.SPEED_Y
        # apply GRAVITY
        self.vel_y += constants.movement.GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:  # verifica se ao clicar, o nosso lado esquerdo saira da tela
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:  # verifica se ao clicar, o nosso lado direito saira da tela
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            dy = screen_height - 110 - self.rect.bottom
        if self.rect.top + dy < 150:
            self.vel_y = 0
            dy = screen_height - 110 - self.rect.bottom

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
