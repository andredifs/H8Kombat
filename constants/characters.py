import pygame

# Load sprites
anao_sheets = [
    pygame.image.load("assets/sprites/anao_movimento.png"),
    pygame.image.load("assets/sprites/anao_soco.png"),
    pygame.image.load("assets/sprites/anao_chute.png"),
]

lula_sheets = [
    pygame.image.load("assets/sprites/lula_movimento.png"),
    pygame.image.load("assets/sprites/lula_soco.png"),
    pygame.image.load("assets/sprites/lula_chute.png"),
]

quinze_sheets = [
    pygame.image.load("assets/sprites/15_movimento.png"),
    pygame.image.load("assets/sprites/15_soco.png"),
    pygame.image.load("assets/sprites/15_chute.png"),
]

# Create fighters
fighters = {
    "anao": anao_sheets,
    "lula": lula_sheets,
    "quinze": quinze_sheets,
}
