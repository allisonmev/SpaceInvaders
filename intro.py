from pygame import display, time, image
from pygame.font import Font


class Button:
    """Open game with introduction of attributes"""
    def __init__(self, settings, screen, msg, y_factor=0.65):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set Attributes
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.alt_color = (0, 255, 0)

        # Set font
        self.font = Font('fonts/Retravant Garden.ttf', 48)

        # Set pos
        self.y_factor = y_factor

        # Set message
        self.msg = msg
        self.msg_image = None
        self.msg_image_rect = None
        self.prep_msg(self.text_color)

    def check_button(self, mouse_x, mouse_y):
        """Allow to check if button is clicked"""
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    def prep_msg(self, color):
        """Allow to display message onto the button and screen"""
        self.msg_image = self.font.render(self.msg, True, color, self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = (self.settings.screen_width // 2)
        self.msg_image_rect.centery = int(self.settings.screen_height * self.y_factor)

    def draw_button(self):
        """Show button on the screen"""
        self.screen.blit(self.msg_image, self.msg_image_rect)


class EnemyDisplay:
    """Format and display the aliens featured in the game"""
    # Set
    def __init__(self, ai_settings, screen, y_start):
        self.screen = screen
        self.settings = ai_settings
        self.aliens = []

        # Load images
        images = [image.load('images/Alien1-1.png'), image.load('images/Alien2-1.png'), image.load('images/Alien3-1.png'), image.load('images/ufo.png')]
        for img in images:
            self.aliens.append((img, img.get_rect()))
        # Set format
        self.example_scores = [
            Subtitle(ai_settings.bg_color, self.screen, '  ' + str(ai_settings.alien_points['1']),
                     text_color=(255, 255, 255)),
            Subtitle(ai_settings.bg_color, self.screen, '  ' + str(ai_settings.alien_points['2']),
                     text_color=(255, 255, 255)),
            Subtitle(ai_settings.bg_color, self.screen, '  ' + str(ai_settings.alien_points['3']),
                     text_color=(255, 255, 255)),
            Subtitle(ai_settings.bg_color, self.screen, '  ???', text_color=(255, 255, 255))
        ]
        # Set format
        self.score_images = []
        self.y_start = y_start
        self.apply_images()

    def apply_images(self):
        """Allows to help prepare for the images later"""
        y_offset = self.y_start
        for a, es in zip(self.aliens, self.example_scores):
            a[1].centery = y_offset
            a[1].centerx = (self.settings.screen_width // 2) - a[1].width
            es.apply_image()
            es.image_rect.centery = y_offset
            es.image_rect.centerx = (self.settings.screen_width // 2) + a[1].width
            y_offset += int(a[1].height * 1.5)

    def display_examples(self):
        """Display and show the aliens on the screen """
        for a in self.aliens:
            self.screen.blit(a[0], a[1])
        for es in self.example_scores:
            es.blitme()


class Title:
    """Title Attributes"""
    def __init__(self, bg_color, screen, text, text_size=56, text_color=(255, 255, 255)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = Font('fonts/Retravant Garden.ttf', text_size)
        self.image = None
        self.image_rect = None

    def apply_image(self):
        """Allow for text to be image to display"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        """Display and show on the screen"""
        self.screen.blit(self.image, self.image_rect)


class Subtitle:
    """Subtitle attributes, not as big as title"""
    def __init__(self, bg_color, screen, text, text_size=48, text_color=(0, 255, 0)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = Font('fonts/Retravant Garden.ttf', text_size)
        self.image = None
        self.image_rect = None

    def apply_image(self):
        """Allow for text to be image to display"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        """Display and show on the screen"""
        self.screen.blit(self.image, self.image_rect)


def level_intro(ai_settings, screen, stats):
    """Display a level intro screen for 1.5 seconds"""
    if stats.game_active:
        level_text = Title(ai_settings.bg_color, screen, 'Level: ' + str(stats.level))
        level_text.apply_image()
        level_text.image_rect.centerx = (ai_settings.screen_width // 2)
        level_text.image_rect.centery = (ai_settings.screen_height // 2) - level_text.image_rect.height
        start_time = time.get_ticks()
        while abs(start_time - time.get_ticks()) <= 1500:
            screen.fill(ai_settings.bg_color)
            level_text.blitme()
            display.flip()


class Intro:
    """Display all features on the opening of the game"""
    def __init__(self, settings, game_stats, screen):
        # Manage the screen of the introduction
        self.settings = settings
        self.game_stats = game_stats
        self.screen = screen

        # Manage the title of the intro and attributes of the text
        self.title = Title(settings.bg_color, self.screen, 'SPACE', text_size=80)
        self.subtitle = Subtitle(settings.bg_color, self.screen, 'INVADERS', text_size=70)
        self.enemy_display = EnemyDisplay(settings, self.screen, self.settings.screen_height // 3)
        self.apply_image()

    def apply_image(self):
        """Allow for text to be image to display"""
        self.title.apply_image()

        # Set the image position of the text image
        self.title.image_rect.centerx = (self.settings.screen_width // 2)
        self.title.image_rect.centery = (self.settings.screen_height // 5) - self.title.image_rect.height
        self.subtitle.apply_image()
        self.subtitle.image_rect.centerx = (self.settings.screen_width // 2)
        self.subtitle.image_rect.centery = (self.settings.screen_height // 5) + (self.title.image_rect.height // 3)

    def show_menu(self):
        """Display and show on the screen"""
        self.title.blitme()
        self.subtitle.blitme()
        self.enemy_display.display_examples()
