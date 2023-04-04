import pygame

pygame.joystick.init()

PLAYER1 = {
    'jump': pygame.K_w,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'defend': pygame.K_s,
    'attack1': pygame.K_r,
}

PLAYER2 = {
    'jump': pygame.K_UP,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'defend': pygame.K_DOWN,
    'attack1': pygame.K_RSHIFT,
}
