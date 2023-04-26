import pygame

def get_font(size: int):
    return pygame.font.Font("assets/font.ttf", size)

def draw_text(surface: pygame.Surface, text, size, text_col, x, y):
    img = get_font(size).render(text, True, text_col)
    img_rect = img.get_rect(center=(x, y))
    return surface.blit(img, img_rect)
