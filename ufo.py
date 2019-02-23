import pygame
from pygame.sysfont import SysFont
from random import choice


class UFO(pygame.sprite.Sprite):
    """Represents a UFO meant to move across the screen at random intervals"""
    def __init__(self, ai_settings, screen, sound=True):
        super().__init__()

        # Set screen
        self.sound = sound
        self.screen = screen
        self.ai_settings = ai_settings
        self.possible_scores = ai_settings.ufo_point_values
        self.score = None

        # Load Image
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        self.score_image = None
        self.font = SysFont(None, 32, italic=True)
        self.prep_score()

        # Sound of UFO
        self.entrance_sound = pygame.mixer.Sound('sounds/ufo.wav')
        self.hit_sound = pygame.mixer.Sound('sounds/ufoHit.wav')
        self.entrance_sound.set_volume(0.6)
        self.channel = ai_settings.ufoRadio

        # Speed of UFO
        self.speed = ai_settings.ufo_speed * (choice([-1, 1]))

        # Starting Position with speed
        self.rect.x = 0 if self.speed > 0 else ai_settings.screen_width
        self.rect.y = ai_settings.screen_height * 0.1

        # When UFO is inactive
        self.dead = False

        # When UFO hit
        self.hit_animated = []
        self.hit_index = None
        self.hit_animated.append(self.score_image)
        self.end_scene = None
        self.wait_interval = 200

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def hit_ufo(self):
        self.channel.stop()
        self.channel.play(self.hit_sound)
        self.dead = True
        self.hit_index = 0
        self.image = self.hit_animated[self.hit_index]
        self.end_scene = pygame.time.get_ticks()

    def died(self):
        self.channel.stop()
        super().kill()

    def get_score(self):
        """Get any score"""
        self.score = choice(self.possible_scores)
        return self.score

    def prep_score(self):
        score_str = str(self.get_score())
        self.score_image = self.font.render(score_str, True, (255, 223, 0), self.ai_settings.bg_color)

    def update(self):
        """Update the UFO functions"""

        # When ufo is not yet dead manage the speed
        if not self.dead:
            self.rect.x += self.speed
            if self.speed > 0 and self.rect.left > self.ai_settings.screen_width:
                self.died()
            elif self.rect.right < 0:
                self.died()
        else:
            # Random movements of ufo
            timer = pygame.time.get_ticks()
            if abs(timer - self.end_scene) > self.wait_interval:
                self.end_scene = timer
                self.hit_index += 1
                if self.hit_index >= len(self.hit_animated):
                    self.died()
                else:
                    # When UFO get hit the image animates through
                    self.image = self.hit_animated[self.hit_index]
                    self.wait_interval += 200
