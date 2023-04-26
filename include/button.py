from pygame import font
from constants import colors

class Button():
    """
    A class to represent a clickable button.

    Attributes:
        image (pygame.Surface): The image to display on the button. If None, the text will be displayed instead.
        x_pos (int): The x coordinate of the button's center.
        y_pos (int): The y coordinate of the button's center.
        font (pygame.font.Font): The font to use for the text on the button.
        base_color (tuple): The color of the text when the button is not being hovered over.
        hovering_color (tuple): The color of the text when the button is being hovered over.
        text_input (str): The text to display on the button.
        text (pygame.Surface): The rendered text surface.
        rect (pygame.Rect): The rectangle of the button's image.
        text_rect (pygame.Rect): The rectangle of the button's text.

    Methods:
        update(screen): Updates the button's appearance on the screen.
        checkForInput(position): Returns True if the given position is inside the button's rectangle, otherwise False.
        changeColor(position): Changes the button's text color depending on whether the given position is inside the button's rectangle.

    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Constructs all the necessary attributes for the Button object.

        Args:
            image (pygame.Surface): The image to display on the button. If None, the text will be displayed instead.
            pos (tuple): The x and y coordinates of the button's center.
            text_input (str): The text to display on the button.
            font (pygame.font.Font): The font to use for the text on the button.
            base_color (tuple): The color of the text when the button is not being hovered over.
            hovering_color (tuple): The color of the text when the button is being hovered over.

        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Updates the button's appearance on the screen.

        Args:
            screen (pygame.Surface): The surface on which to update the button.

        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """
        Checks if the given position is inside the button's rectangle.

        Args:
            position (tuple): The x and y coordinates to check.

        Returns:
            bool: True if the given position is inside the button's rectangle, otherwise False.

        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        """
        Changes the button's text color depending on whether the given position is inside the button's rectangle.

        Args:
            position (tuple): The x and y coordinates to check.

        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def menu_button(text_input, pos):
    """
    Create a menu button object.

    :param text_input: The text displayed on the button.
    :type text_input: str
    :param pos: The position of the button on the screen.
    :type pos: tuple[int, int]
    :return: A Button object.
    :rtype: Button
    """
    return Button(
        None,
        pos,
        text_input,
        font.Font("assets/font.ttf", 50),
        colors.BLUE,
        colors.CYAN
    )
