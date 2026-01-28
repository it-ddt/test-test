"""Модуль мяча."""

import arcade

import random

import config


class Ball(arcade.SpriteSolidColor):
    """Мяч."""

    def __init__(self, x: int, y: int, window_width: int, window_height: int) -> None:
        self.window_width = window_width
        self.window_height = window_height
        width = int(self.window_height * 0.03)
        height = width
        super().__init__(width, height)
        self.center_x = self.start_x = x
        self.center_y = self.start_y = y
        self.color = arcade.color.WHITE
        self.speed = 10
        self.vel_x = 0
        self.vel_y = 0
        self.sounds = dict()
        self.sounds["collide"] = arcade.load_sound(config.SOUND_DIR / "collide.wav")
        self.sounds["score"] = arcade.load_sound(config.SOUND_DIR / "score.wav")
        self.reset()

    def move(self) -> None:
        """Движение."""
        self.center_x += self.vel_x * self.speed
        self.center_y += self.vel_y * self.speed

    def collide_top_bottom(self) -> None:
        """Столкновения с верхней и нижней границами экрана."""
        if self.top <= self.window_height and self.bottom >= 0:
            return
        self.vel_y *= -1
        arcade.play_sound(self.sounds["collide"])

    def reset(self) -> None:
        """Возвращает мяч в центр и выбирает ему случайное направление."""
        self.center_x = self.start_x
        self.center_y = self.start_y
        self.vel_x = random.choice((-1, 1))
        self.vel_y = random.uniform(-1.0, 1.0)
