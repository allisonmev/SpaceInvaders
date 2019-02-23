import pygame
from pygame.font import Font


class Button:

    def __init__(self, screen, msg):
        """Manage button attributes."""
        # Set
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Build the attributes to button
        # Length & color
        self.width = 100
        self.height = 30
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)

        # Add font
        self.font = Font('fonts/Retravant Garden.ttf', 48)

        # Apply rect for the button and center the button attributes
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Allow for button to apply message
        self.apply_msg(msg)
        self.msg_image = None
        self.msg_rect = None

    def apply_msg(self, msg):
        """Apply the message in the center of button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.center = self.rect.center

    def draw_button(self):
        """Construct the button itself"""
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_rect)
