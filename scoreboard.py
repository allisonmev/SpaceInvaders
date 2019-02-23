from pygame.sprite import Group
from ship import Ship
from pygame.font import Font


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for score information
        self.text_color = (255, 255, 0)
        self.font = Font('fonts/Retravant Garden.ttf', 48)
        self.score_image = None
        self.score_rect = None

        self.high_score_image = None
        self.high_score_rect = None

        self.level_image = None
        self.level_rect = None

        self.ships = None

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_level(self):
        """Turn the level into a rendered image"""

        # Load the image
        self.level_image = self.font.render('Level: ' + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # Position on the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Display the number of ships left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 5)
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score(self):
        """Turn score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1))

        # Format the score on the screen
        score_str = 'Score: {:,}'.format(rounded_score)

        # Load the image on the screen
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # Position of the image on the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn high score into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))

        # Format the score on the screen
        high_score_str = 'High Score: {:,}'.format(high_score)

        # Load the high score on the screen
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Position of the image on screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw scores to the screen"""
        # Draw score on screen
        self.screen.blit(self.score_image, self.score_rect)
        # Draw level on screen
        self.screen.blit(self.level_image, self.level_rect)
        # Draw the high score on the screen
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # Draw remaining ships
        self.ships.draw(self.screen)
