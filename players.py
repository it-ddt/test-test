"""Модуль игроков."""

import arcade


class Player(arcade.SpriteSolidColor):
    """Игрок."""

    def __init__(self, window_height: int, is_manual: bool) -> None:
        """Инициализирует игрока."""
        self.window_height = window_height
        height = self.window_height * 0.1
        width = height * 0.3
        color = arcade.color.WHITE
        super().__init__(width, height, color=color)
        self.speed = 10
        self.direction = 0
        self.is_manual = is_manual

    def move(self) -> None:
        """Двигает игрока с ограничениями по верхней и нижней границам экрана."""
        self.center_y += self.speed * self.direction
        if self.top > self.window_height:
            self.top = self.window_height
        if self.bottom < 0:
            self.bottom = 0

    def update(self, delta_time: float, ball_y: int) -> None:
        if self.is_manual:
            return
        if self.center_y > ball_y:
            self.direction = -1
        elif self.center_y < ball_y:
            self.direction = 1
        else:
            self.direction = 0
