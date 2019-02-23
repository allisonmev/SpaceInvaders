import pygame
from pygame import *
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen, alien_type=3):
        """Initialize alien and set starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alien_type = alien_type

        # Load the alien image and set its rect attribute.
        self.images = None
        self.image = None
        self.image_index = None
        self.hit_index = None
        self.hit_animation = None
        self.end_structure = None
        self.rect = None
        self.setImages()

        # Assign sounds to alien feature
        self.hit_sound = pygame.mixer.Sound('sounds/alienHit.wav')
        self.shoot_sound = pygame.mixer.Sound('sounds/alienShoot.wav')
        self.hit_sound.set_volume(0.2)
        self.shoot_sound.set_volume(0.2)
        self.channel = ai_settings.alienRadio

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact position
        self.x = float(self.rect.x)

        # Set Alien when active
        self.dead = False

    def shoot_fire(self):
        """Begin to play sound effects when shoot"""
        self.channel.play(self.shoot_sound)

    def setImages(self):
        """Set images into arrays"""
        if self.alien_type == 1:
            self.images = [pygame.image.load('images/Alien1-1.png'), pygame.image.load('images/Alien1-2.png')]
            self.hit_animation = [pygame.image.load('images/Alien1E1.png'), pygame.image.load('images/Alien1E2.png'),
                                  pygame.image.load('images/Alien1E3.png')]
        elif self.alien_type == 2:
            self.images = [pygame.image.load('images/Alien2-1.png'), pygame.image.load('images/Alien2-2.png')]
            self.hit_animation = [pygame.image.load('images/Alien2E1.png'), pygame.image.load('images/Alien2E2.png'),
                                  pygame.image.load('images/Alien2E3.png')]
        else:
            self.images = [pygame.image.load('images/Alien3-1.png'), pygame.image.load('images/Alien3-2.png')]
            self.hit_animation = [pygame.image.load('images/Alien3E1.png'), pygame.image.load('images/Alien3E2.png'),
                                  pygame.image.load('images/Alien3E3.png')]

        # Set images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.end_structure = pygame.time.get_ticks()

    def blitme(self):
        """Draw alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()

        # Measures the surround
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        else:
            return False

    def bullet_collide(self):
        """Set when alien hits"""
        self.dead = True
        self.hit_index = 0
        self.image = self.hit_animation[self.hit_index]
        self.end_structure = pygame.time.get_ticks()
        self.channel.play(self.hit_sound)

    def update(self):
        """Allow to move the alien right or left and animate through frames"""

        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        time_test = pygame.time.get_ticks()

        # Loop through frames
        if not self.dead:
            if abs(self.end_structure - time_test) > 1000:
                self.end_structure = time_test
                self.image_index = (self.image_index + 1) % len(self.images)
                self.image = self.images[self.image_index]

        # Make sure to allow for delay in the animations during loop
        else:
            if abs(self.end_structure - time_test) > 15:
                self.end_structure = time_test
                self.hit_index += 1
                if self.hit_index >= len(self.hit_animation):
                    self.kill()
                else:
                    self.image = self.hit_animation[self.hit_index]
