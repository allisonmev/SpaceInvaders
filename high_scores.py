from intro import Title


class HighScoreScreen:
    """Display High Score for the High Score Screen when pressed button"""
    def __init__(self, ai_settings, screen):
        # To apply scores
        self.score_text = []

        # Add title of the scores
        self.score_text.append(Title(ai_settings.bg_color, screen, 'High Scores'))

        # Print text onto the center of the screen when button pressed
        for text in self.score_text:
            text.apply_image()
            text.image_rect.centerx = ai_settings.screen_width/2

    def show_scores(self):
        """Show scores of the high scores"""
        for text in self.score_text:
            text.blitme()
