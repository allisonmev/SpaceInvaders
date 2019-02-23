import pygame
import random
import sys
from alien import Alien
from alien_bullet import AlienBullet
from bullet import Bullet
from ufo import UFO
from high_scores import HighScoreScreen
from intro import Button, Intro, level_intro
from pygame import *


def check_events(ai_settings, screen, stats, ship, bullets):
    """Respond to key presses and mouse events"""
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            sys.exit()
        elif events.type == pygame.KEYDOWN:
            check_keydown_events(events, ai_settings, screen, stats.game_active, ship, bullets)
        elif events.type == pygame.KEYUP:
            check_keyup_events(events, ship)


def check_keydown_events(events, ai_settings, screen, game_active, ship, bullets):
    """Handle key presses"""
    # When right
    if events.key == pygame.K_RIGHT:
        ship.moving_right = True
    # When left
    elif events.key == pygame.K_LEFT:
        ship.moving_left = True
    # Helps prevent sounds from occurring when game is not active
    # When space
    elif events.key == pygame.K_SPACE and game_active:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif events.key == pygame.K_q:
        sys.exit()


def check_keyup_events(events, ship):
    """Handle key releases"""
    # When right
    if events.key == pygame.K_RIGHT:
        ship.moving_right = False
    # When left
    elif events.key == pygame.K_LEFT:
        ship.moving_left = False


def start_game(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets):
    """Start a new game when the play button is clicked"""

    # Mouse disappears when over the game screen
    pygame.mouse.set_visible(False)

    # Reset the game settings for new game
    ai_settings.initialize_dynamic_settings()

    # Reset game stats for new game
    stats.reset_stats()

    # New game begins
    stats.game_active = True

    # Reset the scores
    sb.prep_score()
    sb.prep_high_score()

    # Reset level image
    sb.prep_level()

    # Reset ship image
    sb.prep_ships()

    # Remove aliens, alien bullets, and bullets
    aliens.empty()
    bullets.empty()
    alien_bullets.empty()

    # Reset alien fleet
    create_fleet(ai_settings, screen, ship, aliens)
    stats.next_speedup = len(aliens) - (len(aliens) // 5)
    stats.aliens_left = len(aliens)

    # Reset ship position
    ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if the limit not reached already"""
    if len(bullets) < ai_settings.bullets_allowed:
        # Create new bullet
        new_bullet = Bullet(ai_settings, screen, ship)
        # Ship fire bullets
        ship.fire_weapon()
        bullets.add(new_bullet)


def fire_random_alien_bullet(ai_settings, screen, aliens, alien_bullets):
    """Random bullets fire from aliens randomly"""
    # Alien fire randomly
    firing_alien = random.choice(aliens.sprites())
    if len(alien_bullets) < ai_settings.alien_bullet_allowed and (ai_settings.alien_bullet_stamp is None or (abs(pygame.time.get_ticks() - ai_settings.alien_bullet_stamp) > ai_settings.alien_bullet_time)):
        new_alien_bullet = AlienBullet(ai_settings, screen, firing_alien)
        # Fire from alien
        firing_alien.shoot_fire()
        # Create new bullet
        alien_bullets.add(new_alien_bullet)


def update_alienBullet(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo):
    """Manages all bullets and remove bullets that are no longer visible"""
    # Create bullets
    bullets.update()
    alien_bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.bottom > ai_settings.screen_height:
            alien_bullets.remove(alien_bullet)

    # Check for functions when contact
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)
    check_ship_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)


def alien_collision_check(bullet, alien):
    """When alien get hits and alien will be disappear"""
    if alien.dead:
        return False
    return pygame.sprite.collide_rect(bullet, alien)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo):
    """Check that any aliens have been hit, handle empty fleet condition"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False, collided=alien_collision_check)
    # When collisions occur to aliens
    if collisions:
        for aliens_hit in collisions.values():
            for a in aliens_hit:
                # Set scores
                stats.score += ai_settings.alien_points[str(a.alien_type)]
                a.bullet_collide()
            sb.prep_score()
        check_high_score(stats, sb)
    # When collisons occur to ufo
    ufo_collide = pygame.sprite.groupcollide(bullets, ufo, True, False, collided=alien_collision_check)
    if ufo_collide:
        for ufo in ufo_collide.values():
            # Update scores
            for u in ufo:
                stats.score += u.score
                u.hit_ufo()
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        if ufo:
            for u in ufo.sprites():
                u.died()
        # Manages the alien bullets and manages level increases
        alien_bullets.empty()
        bullets.empty()
        stats.level += 1
        level_intro(ai_settings, screen, stats)
        # Manages music speed
        ai_settings.increase_base_speed()
        # Manages alien speed
        ai_settings.reset_alien_speed()
        # Calls to show scoreboard
        sb.prep_level()
        # Crate the fleet of aliens
        create_fleet(ai_settings, screen, ship, aliens)
        stats.next_speedup = len(aliens) - (len(aliens) // 5)
    stats.aliens_left = len(aliens)
    if stats.aliens_left <= stats.next_speedup and ai_settings.alien_speed_factor < ai_settings.alien_speed_limit:
        # Increases speed of aliens when certain aliens left
        ai_settings.increase_alien_speed()
        stats.next_speedup = stats.aliens_left - (stats.aliens_left // 5)


def check_ship_alien_bullet_collisions(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo):
    """Check that any alien bullets have collided with the ship"""
    collide = pygame.sprite.spritecollideany(ship, alien_bullets)
    # Manages the collision of the ship
    if collide:
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)


def check_bunker_collisions(alien_bullets, bullets, bunkers):
    """Manages the bunker collisions when bullets hit"""
    # Collision when ship hit the block
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, False)
    # Collision when block will be false
    for b_list in collisions.values():
        for block in b_list:
            block.blockHit(top=False)
    # Collision when alien bullet hits block
    collisions = pygame.sprite.groupcollide(alien_bullets, bunkers, True, False)
    # Collision when block will be true
    for b_list in collisions.values():
        for block in b_list:
            block.blockHit(top=True)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, ufo):
    """Respond to ship being hit by an alien"""
    # Update the alien when hit
    if ufo:
        for u in ufo.sprites():
            u.died()
    # Manges the when ship gets hit
    ship.death()
    ship.update()

    # Manges when ship animated if dead
    while ship.dead:
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        pygame.display.flip()
        ship.update()

    # Subtract lives when ship hit
    if stats.ships_left > 0:
        # Decrement lives
        stats.ships_left -= 1

        # Remove aliens, alien bullets, and bullets off the screen
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        # Reset aliens and speed
        ai_settings.reset_alien_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        stats.next_speedup = len(aliens) - (len(aliens) // 5)
        stats.aliens_left = len(aliens.sprites())
        ship.center_ship()

        # Update the ships
        sb.prep_ships()
    else:
        # Manage the music
        ai_settings.stop_bgm()
        pygame.mixer.music.load('sounds/gameOver.wav')
        pygame.mixer.music.play()

        # Manage when functions the game ends
        stats.game_active = False
        pygame.mouse.set_visible(True)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that can fit in a row"""
    # Create aliens depend on the measure
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2.5 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that can fit in a row"""
    # Depending on the measure
    available_space_y = (ai_settings.screen_height - (5 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2.5 * alien_height))
    return number_rows


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)
            break


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row"""

    # Organize the aliens by rows
    if row_number < 2:
        alien_type = 1
    elif row_number < 4:
        alien_type = 2
    else:
        alien_type = 3

    # Create aliens
    alien = Alien(ai_settings, screen, alien_type)

    # Set aliens attributes and positions
    alien_width = alien.rect.width
    alien.x = alien_width + 1.25 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.25 * alien.rect.height * row_number
    alien.rect.y += int(ai_settings.screen_height / 8)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creates a full fleet of aliens"""

    # Space the aliens by width and height
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create an alien and place certain alien in row
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet down, and change the fleets direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """Respond in the event any aliens have reached an edge of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            # Allow to change direction when reach end of edge
            change_fleet_direction(ai_settings, aliens)
            break


def create_random_ufo(ai_settings, screen):
    """Create a UFO 80% of the time and show up"""
    ufo = None

    # Set random timing to ufo 80% of the time
    if random.randrange(0, 100) <= 80:
        ufo = UFO(ai_settings, screen)
    time_stamp = pygame.time.get_ticks()

    return time_stamp, ufo


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo):
    """Check if any aliens in the fleet have reached an edge, then update the positions of all aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Update the alien collisions when ship is hit
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, ufo)
    # Allows aliens to fire bullets
    if aliens.sprites():
        fire_random_alien_bullet(ai_settings, screen, aliens, alien_bullets)


def ufo_event_check(ai_settings, screen, ufo_group):
    """Manage to create ufo and add to the groups of ufo when it is ready """
    # Allow to create ufo
    if not ai_settings.last_ufo and not ufo_group:
        ai_settings.last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        # Add to ufo group when if the ufo is not in group
        if n_ufo:
            ufo_group.add(n_ufo)
    # Random ufo
    elif abs(pygame.time.get_ticks() - ai_settings.last_ufo) > ai_settings.ufo_min_interval and not ufo_group:
        ai_settings.last_ufo, n_ufo = create_random_ufo(ai_settings, screen)
        # Add to ufo group when if the ufo is not in group
        if n_ufo:
            ufo_group.add(n_ufo)


def check_high_score(stats, sb):
    """Check to see if there's a new high score and compare the scores from prev."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, bullets, bunkers, ufo_group):
    """Update images on the screen and flip to new screen"""
    if stats.game_active:
        ufo_event_check(ai_settings, screen, ufo_group)
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Redraw all alien bullets
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_alienBullet()
    if ufo_group:
        ufo_group.update()
        for ufo in ufo_group.sprites():
            ufo.blitme()
    # Redraw all aliens
    aliens.draw(screen)
    check_bunker_collisions(alien_bullets, bullets, bunkers)

    # Draw score info
    sb.show_score()
    ship.blitme()

    # Make recently bunker
    bunkers.update()

    # Make most recently drawn screen
    pygame.display.flip()


def high_score_screen(ai_settings, screen):
    """Display all high scores in a separate screen with a back button"""
    # Set the screen attributes
    hs_screen = HighScoreScreen(ai_settings, screen)
    back_button = Button(ai_settings, screen, 'Back To Menu', y_factor=0.85)

    while True:
        # Functions of the game when key presses touched
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
            elif events.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_button(*pygame.mouse.get_pos()):
                    return True

        screen.fill(ai_settings.bg_color)
        # Allow to show the scores on the high score screen
        hs_screen.show_scores()
        # Redraw button
        back_button.draw_button()
        # Display past
        pygame.display.flip()


def opening_screen(ai_settings, game_stats, screen):
    """Display the menu in the beginning"""

    # Set up screen attributes
    menu = Intro(ai_settings, game_stats, screen)
    play_button = Button(ai_settings, screen, 'Play Game', y_factor=0.70)
    hs_button = Button(ai_settings, screen, 'High Scores', y_factor=0.80)
    intro = True

    # Manages the key presses of the game
    while intro:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
            elif events.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                game_stats.game_active = play_button.check_button(click_x, click_y)
                intro = not game_stats.game_active
                if hs_button.check_button(click_x, click_y):
                    ret_hs = high_score_screen(ai_settings, screen)
                    if not ret_hs:
                        return False

        screen.fill(ai_settings.bg_color)
        # Allow the menu to display on the top layer
        menu.show_menu()
        # Draw the button on the main screen
        hs_button.draw_button()
        play_button.draw_button()

        # Display past
        pygame.display.flip()

    return True


def music_BG(ai_settings, stats):
    """Allow for background music to play when game is ONLY ACTIVE"""
    if stats.game_active:
        ai_settings.continue_bgm()
