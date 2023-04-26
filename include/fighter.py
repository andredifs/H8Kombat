import pygame
import constants.movement
from constants.colors import RED
import constants.controls

class Fighter():
    """A class representing a fighter in the game.

    Attributes:
        rect (pygame.Rect): A rectangle that represents the fighter's position and size.
        initial_pos (tuple): A tuple of two integers representing the initial position of the fighter.
        surface (pygame.Surface): The surface on which the fighter is drawn.
        vel_y (float): The vertical velocity of the fighter.
        flip (bool): A boolean value indicating whether the fighter is flipped horizontally.
        jumping (bool): A boolean value indicating whether the fighter is currently jumping.
        attacking (bool): A boolean value indicating whether the fighter is currently attacking.
        attack_type (int): An integer representing the type of attack the fighter is performing.
        attack_cooldown (int): The remaining time until the fighter can perform another attack.
        defending (bool): A boolean value indicating whether the fighter is currently defending.
        defend_cooldown (int): The remaining time until the fighter can stop defending.
        health (int): The current health of the fighter.
        dead (bool): A boolean value indicating whether the fighter is dead.
        controls (dict): A dictionary containing the control mappings for the fighter.
        target (Fighter): The opponent that the fighter is currently facing.
        score (int): The current score of the fighter.
        color (tuple): A tuple of three integers representing the RGB color values of the fighter.

    Methods:
        __init__(self, x, y, surface, color): Initializes a new instance of the Fighter class.
    """

    def __init__(self, x, y, surface, color):
        """Initializes a new instance of the Fighter class.

        Args:
            x (int): The x-coordinate of the fighter's starting position.
            y (int): The y-coordinate of the fighter's starting position.
            surface (pygame.Surface): The surface on which the fighter will be drawn.
            color (tuple): A tuple of three integers representing the RGB color values of the fighter.
        """
        self.rect = pygame.Rect((x, y, 80, 180))
        self.initial_pos = (x, y)
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
        self.dead: bool = False
        self.controls: dict = {}
        self.target: Fighter = None
        self.score: int = 0
        self.color = color

    def move(self, screen_width, screen_height):
        """
        This method moves the fighter according to the input controls.
        Args:
            screen_width (int): The width of the game screen.
            screen_height (int): The height of the game screen.
        Raises:
            Exception: If the target is not defined.
        """
        if not self.target:
            raise Exception('Target not defined')

        dx, dy = 0, 0

        key = pygame.key.get_pressed()

        if self.attacking is False and self.defending is False:
            # defend
            if key[self.controls['defend']]:
                self.defend()

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
        """
        This method makes the fighter jump.
        """
        if self.jumping is False:
            self.vel_y = -constants.movement.SPEED_Y
            self.jumping = True

    def attack(self):
        """
        This method executes an attack from the fighter.
        """
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
            self.target.health -= 10
            if self.target.health == 0:
                self.target.dead = True

        pygame.draw.rect(self.surface, RED, attacking_rect)

    def defend(self):
        """Defend method for the fighter.

        Raises:
            TypeError: If attack cooldown or defend cooldown is active.

        Returns:
            None
        """
        if self.attack_cooldown > 0 or self.defend_cooldown > 0:
            raise TypeError("Attack or Defend cooldown is active.")

        self.defending = True
        self.defend_cooldown = constants.movement.DEFEND_COOLDOWN

    def update_pos(self, dx, dy, screen_width, screen_height):
        """Update fighter's position.

        Args:
            dx (int): Change in x direction of the fighter's position.
            dy (int): Change in y direction of the fighter's position.
            screen_width (int): Width of the game screen.
            screen_height (int): Height of the game screen.

        Returns:
            None
        """
        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
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
        """Draws the fighter on the game screen.

        Returns:
            None
        """
        pygame.draw.rect(self.surface, self.color, self.rect)

    def set_target(self, target):
        """Set the opponent for the fighter.

        Args:
            target (Fighter): The opponent.

        Returns:
            None
        """
        self.target = target

    def set_controls(self, controls):
        """Set the control keys for the fighter.

        Args:
            controls (dict): A dictionary containing control keys for the fighter.

        Returns:
            None
        """
        self.controls = controls

    def reset(self):
        """Reset the fighter's attributes.

        Returns:
            None
        """
        self.vel_y = 0
        self.flip = False
        self.jumping = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.defending = False
        self.defend_cooldown = 0
        self.health = 100
        self.dead = False
        self.rect.x, self.rect.y = self.initial_pos
