from pygame import *


class Settings:
    """Stores settings for Alien Invasion"""
    def __init__(self):
        # Screen Settings
        self.screen_width = 1000
        self.screen_height = 700
        # bg to black
        self.bg_color = (0, 0, 0)

        # Ship Settings
        # Ship Lives Remaining
        self.ship_limit = 3
        self.ship_speed_factor = None

        # Bullet Settings
        self.bullet_speed_factor = 10
        self.bullet_width = 5
        self.bullet_height = 8
        self.bullet_color = (0, 255, 0)
        self.bullets_allowed = 10
        # Alien Bullet Settings
        self.alien_bullet_speed_factor = None
        self.alien_bullet_color = (224, 255, 255)
        self.alien_bullet_allowed = 2

        # Bunker Settings
        self.bunkerSize = 8
        self.bunkerColor = (0, 255, 0)

        # Sound Settings
        self.radio = 5
        self.shipRadio = mixer.Channel(0)
        self.alienRadio = mixer.Channel(1)
        self.hitRadio = mixer.Channel(2)
        self.ufoRadio = mixer.Channel(3)
        self.musicRadio = mixer.Channel(4)
        self.normal_music_interval = 900
        self.music_interval = self.normal_music_interval
        self.music_speedup = 50
        self.musicBG = [mixer.Sound('sounds/sound1.wav'), mixer.Sound('sounds/sound2.wav'), mixer.Sound('sounds/sound3.wav'), mixer.Sound('sounds/sound4.wav'),
                        mixer.Sound('sounds/sound1.wav'), mixer.Sound('sounds/sound4.wav'), mixer.Sound('sounds/sound1.wav')]
        self.bgm_index = None
        self.last_beat = None

        # Aliens
        self.normal_alien_speed = 3
        self.alien_speed_limit = None
        self.alien_base_limit = None
        self.alien_speed_factor = None
        self.ufo_speed = None
        self.last_ufo = None
        self.ufo_min_interval = 10000
        self.fleet_drop_speed = 3
        self.fleet_direction = None
        self.alien_points = None
        self.ufo_point_values = [50, 100, 150]
        self.alien_bullet_stamp = None
        self.alien_bullet_time = 1000
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.initialize_audio_settings()

    def initialize_dynamic_settings(self):
        """Initialize that change while the game is active"""

        self.ship_speed_factor = 30
        self.bullet_speed_factor = 10
        self.alien_bullet_speed_factor = 10
        self.alien_speed_factor = self.normal_alien_speed
        self.alien_speed_limit = self.alien_speed_factor * 5
        self.alien_base_limit = self.alien_speed_limit / 2
        self.ufo_speed = self.alien_speed_factor * 2
        self.fleet_direction = 1

        # Scoring of aliens
        self.alien_points = {'1': 10, '2': 20, '3': 40}

    def initialize_audio_settings(self):
        mixer.init()
        mixer.set_num_channels(self.radio)
        self.musicRadio.set_volume(0.7)

    def continue_bgm(self):
        """Background Music"""
        if not self.last_beat:
            self.bgm_index = 0
            self.musicRadio.play(self.musicBG[self.bgm_index])
            self.last_beat = time.get_ticks()
        elif abs(self.last_beat - time.get_ticks()) > self.music_interval and not self.musicRadio.get_busy():
            # Music continuing
            self.bgm_index = (self.bgm_index + 1) % len(self.musicBG)
            self.musicRadio.play(self.musicBG[self.bgm_index])
            self.last_beat = time.get_ticks()

    def stop_bgm(self):
        """No Music"""
        self.musicRadio.stop()
        self.last_beat = None
        self.bgm_index = None

    def increase_base_speed(self):
        """Increase the starting speed for aliens"""
        if self.normal_alien_speed < self.alien_base_limit:
            self.normal_alien_speed *= self.speedup_scale
            self.normal_music_interval -= self.music_speedup

    def increase_alien_speed(self):
        """Increase alien and music speed"""
        self.alien_speed_factor *= self.speedup_scale
        self.music_interval -= self.music_speedup

    def reset_alien_speed(self):
        """Reset alien and music speed back to its base value"""
        self.alien_speed_factor = self.normal_alien_speed
        self.music_interval = self.normal_music_interval
