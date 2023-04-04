import pygame
import constants.movement
from constants.colors import BLUE, RED

class Fighter():
    def __init__(self, x, y, surface):
        self.rect = pygame.Rect((x, y, 80, 180))  # create a rect of fighter
        self.surface: pygame.Surface = surface
        self.vel_y: float = 0
        self.jumping: bool = False
        self.attacking: bool = False
        self.attack_type: int = 0
        self.attack_cooldown: int = 0
        self.health: int = 100
        self.target: Fighter  # the opponent

    def move(self, screen_width, screen_height):
        if not self.target:
            raise 'Target not defined'

        dx, dy = 0, 0

        key = pygame.key.get_pressed()

        if self.attacking is False:
            # movement
            if key[pygame.K_a]:
                dx = -constants.movement.SPEED_X
            if key[pygame.K_d]:
                dx = constants.movement.SPEED_X

            # jump
            if key[pygame.K_w]:
                self.jump()

            # attack
            if key[pygame.K_r] or key[pygame.K_t]:
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

                self.attack()

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attacking = False

        self.update_pos(dx, dy, screen_width, screen_height)

    def jump(self):
        if self.jumping is False:
            self.vel_y = -constants.movement.SPEED_Y
            self.jumping = True

    def attack(self):
        if self.attack_cooldown > 0:
            return

        self.attacking = True
        self.attack_cooldown = 60

        attacking_rect = pygame.Rect(
            self.rect.centerx,
            self.rect.y,
            2 * self.rect.width,
            self.rect.height
        )

        if attacking_rect.colliderect(self.target.rect):
            self.target.health -= 5

        pygame.draw.rect(self.surface, RED, attacking_rect)

    def update_pos(self, dx, dy, screen_width, screen_height):
        # ensure player stays on screen
        if self.rect.left + dx < 0:  # verifica se ao clicar, o nosso lado esquerdo saira da tela
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:  # verifica se ao clicar, o nosso lado direito saira da tela
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jumping = False
            dy = screen_height - 110 - self.rect.bottom

        # apply gravity
        self.vel_y += constants.movement.GRAVITY
        dy += self.vel_y

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        pygame.draw.rect(self.surface, BLUE, self.rect)

    def set_target(self, target):
        self.target = target
