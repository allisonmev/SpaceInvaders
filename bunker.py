from random import randrange
from pygame import *
from pygame.sprite import Sprite


class setBunker(Sprite):
    """Create bunker"""
    # Set features
    def __init__(self, ai_settings, screen, row, col):
        super().__init__()
        self.screen = screen
        self.height = ai_settings.bunkerSize
        self.width = ai_settings.bunkerSize
        self.color = ai_settings.bunkerColor
        self.row = row
        self.col = col
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.dmg = False

    def blockHit(self, top):
        """When hit allow pixels to disarray(transparent)"""
        # Note: Transparency = 0, 0, 0, 0
        if not self.dmg:
            pix = PixelArray(self.image)
            if top:
                for i in range(self.height * 3):
                    pix[randrange(0, self.width - 1), randrange(0, self.height // 2)] = (0, 0, 0, 0)
            else:
                for i in range(self.height * 3):
                    pix[randrange(0, self.width - 1), randrange(self.height // 2, self.height - 1)] = (0, 0, 0, 0)
            self.dmg = True
        else:
            self.kill()

    def update(self):
        self.screen.blit(self.image, self.rect)


def drawBunker(ai_settings, screen, position):
    """Draw bunker at the certain position"""
    bunker = sprite.Group()
    for row in range(5):
        # Will allow to draw the bunker
        for col in range(9):
            if not ((row > 3 and (1 < col < 7)) or
                    (row > 2 and (2 < col < 6)) or
                    (row == 0 and (col < 1 or col > 7))):
                block = setBunker(ai_settings, screen, row, col)
                block.rect.x = int(ai_settings.screen_width * 0.15) + (250 * position) + (col * block.width)
                block.rect.y = int(ai_settings.screen_height * 0.8) + (row * block.height)
                bunker.add(block)
    return bunker
