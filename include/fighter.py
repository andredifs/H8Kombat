import pygame
import constants.movement
import constants.controls

class Fighter():
    def __init__(self, x, y, surface, sprites, size_y=330):
        self.rect = pygame.Rect((x, y, 250, 200))  # create a rect of fighter
        self.sprites: list[pygame.Surface] = sprites
        self.size_y = size_y
        self.animations = self.load_sprites()
        self.update_time = pygame.time.get_ticks()
        self.action = 0  # 0 = idle, 1 = attack1, 2 = attack2
        self.frame = 0
        self.image = self.animations[self.action][self.frame]
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

    def load_sprites(self):
        animation_list = []

        for sprite in self.sprites:
            temp_list = []
            for image in range(5):
                temp_img = sprite.subsurface(image * 250, 0, 250, self.size_y)
                temp_img = pygame.transform.scale(temp_img, (250, 200))
                temp_list.append(temp_img)

            animation_list.append(temp_list)

        return animation_list

    def move(self, screen_width, screen_height):
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
                self.attack_type = 1
                self.attack()

            if key[self.controls['attack2']]:
                self.attack_type = 2
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
            self.rect.centerx - (self.rect.width / 2 * self.flip),
            self.rect.y,
            self.rect.width / 2,
            self.rect.height
        )

        if attacking_rect.colliderect(self.target.rect) and self.target.defending is False:
            self.target.health -= 10
            if self.target.health == 0:
                self.target.dead = True

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

    def update(self):
        animation_cooldown = 200
        # update image
        self.image = self.animations[self.action][self.frame]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            if self.attacking:
                if self.attack_type == 1:
                    self.update_action(1)
                else:
                    self.update_action(2)
            else:
                self.update_action(0)

            if self.frame < 4:
                self.frame += 1
            else:
                self.frame = 0

            self.update_time = pygame.time.get_ticks()

    def draw(self):
        """Draws the fighter on the game screen.

        Returns:
            None
        """
        img = pygame.transform.flip(self.image, self.flip, False)
        self.surface.blit(img, (self.rect.x, self.rect.y))

    def set_target(self, target):
        self.target = target

    def set_controls(self, controls):
        """Set the control keys for the fighter.

        Args:
            controls (dict): A dictionary containing control keys for the fighter.

        Returns:
            None
        """
        self.controls = controls

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

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
