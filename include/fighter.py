import pygame
import constants.movement
from constants.colors import RED
import constants.controls

class Fighter():
    def __init__(self, x, y, surface, color):
        self.rect = pygame.Rect((x, y, 80, 180))  # create a rect of fighter
        self.surface: pygame.Surface = surface
        self.vel_y: float = 0
        self.flip: bool = False
        self.jumping: bool = False
        self.attacking: bool = False
        self.attack_type: int = 0
        self.attack_cooldown: int = 0
        self.defending: bool = False
        self.defend_cooldown: int = 0
        self.health: int = 100
        self.target: Fighter  # the opponent
        self.controls: dict

        # color
        self.color = color

    def move(self, screen_width, screen_height):
        if not self.target:
            raise 'Target not defined'

        dx, dy = 0, 0

        key = pygame.key.get_pressed()

        if self.attacking is False and self.defending is False:
            # defend
            if key[self.controls['defend']]:
                self.defending = True
                self.defend_cooldown = constants.movement.DEFEND_COOLDOWN

            # attack
            if key[self.controls['attack1']]:
                if key[self.controls['attack1']]:
                    self.attack_type = 1

                self.attack()

            # movement
            if key[self.controls['left']]:
                dx = -constants.movement.SPEED_X
            if key[self.controls['right']]:
                dx = constants.movement.SPEED_X

            # jump
            if key[self.controls['jump']]:
                self.jump()

        # apply defend cooldown
        if self.defend_cooldown > 0:
            self.defend_cooldown -= 1
        else:
            self.defending = False

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
        if self.attack_cooldown > 0 or self.defend_cooldown > 0:
            return

        self.attacking = True
        self.attack_cooldown = constants.movement.ATTACK_COOLDOWN

        attacking_rect = pygame.Rect(
            self.rect.centerx - (2 * self.rect.width * self.flip),
            self.rect.y, 2 * self.rect.width,
            self.rect.height
        )

        if attacking_rect.colliderect(self.target.rect) and self.target.defending is False:
            self.target.health -= 5

        pygame.draw.rect(self.surface, RED, attacking_rect)

    def defend(self):
        if self.attack_cooldown > 0 or self.defend_cooldown > 0:
            return
        self.defending = True
        self.defend_cooldown = constants.movement.DEFEND_COOLDOWN

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

        # ensure players face each other
        if self.target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply gravity
        self.vel_y += constants.movement.GRAVITY
        dy += self.vel_y

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def set_target(self, target):
        self.target = target

    def set_controls(self, controls):
        self.controls = controls
