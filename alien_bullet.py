import pygame
from pygame import *
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """A class to manage bullets fired from the aliens"""
    def __init__(self, ai_settings, screen, alien):
        # Set Screen
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.top

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

        # Store bullets attributes
        self.color = ai_settings.alien_bullet_color
        self.speed_factor = ai_settings.alien_bullet_speed_factor

    def update(self):
        """Move the beam DOWN the screen"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_alienBullet(self):
        """Draw the beam on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
