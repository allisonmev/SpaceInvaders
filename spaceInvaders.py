import pygame

import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from scoreboard import Scoreboard
from bunker import drawBunker


def run_game():
    # Make Game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Space Invaders')
    clock = pygame.time.Clock()

    # Make Ship
    ship = Ship(ai_settings, screen)

    # Make Alien group
    aliens = Group()

    # Make UFO
    ufo = Group()

    # Make Bullets
    bullets = Group()

    # Make Alien bullets
    alien_bullets = Group()

    # Make fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Make bunker group
    bunkers = Group(drawBunker(ai_settings, screen, 0), drawBunker(ai_settings, screen, 1),
                    drawBunker(ai_settings, screen, 2), drawBunker(ai_settings, screen, 3))

    # Feature game stats and scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    while True:
        clock.tick(120)

        # Set processes of when game opens/closes
        if not stats.game_active:
            if not gf.opening_screen(ai_settings, stats, screen):
                pygame.quit()
                break
            else:
                gf.start_game(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets)
        gf.check_events(ai_settings, screen, stats, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_alienBullet(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)

        gf.music_BG(ai_settings, stats)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, bunkers, ufo)


run_game()
