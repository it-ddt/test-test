"""Игра Pong."""

import arcade

from ball import Ball
from players import Player

import config


class MenuView(arcade.View):
    """Представление меню: режимы игры + выход."""

    def __init__(self) -> None:
        super().__init__()
        arcade.load_font(config.FONT_DIR / config.FONT_FILE)
        texts_menu = (
            "ESC - выход из игры",
            "3 - компьютер VS компьютер",
            "2 - человек VS человек",
            "1 - человек VS компьютер",
        )
        self.texts = []

        text_y = self.height // (len(texts_menu) + 1)
        for text_menu in texts_menu:
            text = arcade.Text(
                text_menu,
                self.width // 2,
                text_y,
                color=arcade.color.WHITE,
                font_size=self.height * 0.04,  # TODO: в конфиг?
                anchor_x="center",
                anchor_y="center",
                font_name=config.FONT_FAMILY,
            )
            self.texts.append(text)
            text_y += self.height // (len(texts_menu) + 1)

        self.music = arcade.Sound(config.SOUND_DIR / "music_loop.mp3")
        self.music_player = self.music.play(loop=True)

    def on_hide_view(self):
        self.music_player.pause()

    def on_key_press(self, symbol, _) -> None:
        """Реакция на нажатия клавиш."""
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
        elif symbol == arcade.key.KEY_1:
            view = GameView(True, False)
            window.show_view(view)
        elif symbol == arcade.key.KEY_2:
            view = GameView(True, True)
            window.show_view(view)
        elif symbol == arcade.key.KEY_3:
            view = GameView(False, False)
            window.show_view(view)

    def on_draw(self):
        self.clear()
        for text in self.texts:
            text.draw()


class GameView(arcade.View):
    """Представление игры."""

    def __init__(self, player_1_is_manual: bool, player_2_is_manual: bool):
        """Инициализирует игру со списком спрайтов: две ракетки и мяч."""
        super().__init__()
        self.sprites: arcade.SpriteList[Player] = arcade.SpriteList()
        self.player_1 = Player(self.height, player_1_is_manual)
        self.player_1.left = self.width * 0.1
        self.player_1.center_y = self.height // 2

        self.player_2 = Player(self.height, player_2_is_manual)
        self.player_2.right = self.width * 0.9
        self.player_2.center_y = self.height // 2

        self.players = arcade.SpriteList()
        self.players.append(self.player_1)
        self.players.append(self.player_2)

        x = self.width // 2
        y = self.height // 2
        self.ball = Ball(x, y, self.width, self.height)

        self.score_p1 = arcade.Text(
            "0",
            self.width * 0.25,
            self.height * 0.9,
            font_size=50,
            font_name=config.FONT_FAMILY,
            anchor_x="center",
        )
        self.score_p2 = arcade.Text(
            "0",
            self.width * 0.75,
            self.height * 0.9,
            font_size=50,
            font_name=config.FONT_FAMILY,
            anchor_x="center",
        )

        self.sprites.append(self.player_1)
        self.sprites.append(self.player_2)
        self.sprites.append(self.ball)

    def on_key_press(self, symbol, modifiers):
        """Реакция на нажатия клавиш."""
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
        if self.player_1.is_manual:
            if symbol == arcade.key.W:
                self.player_1.direction = 1
            elif symbol == arcade.key.S:
                self.player_1.direction = -1
        if self.player_2.is_manual:
            if symbol == arcade.key.UP:
                self.player_2.direction = 1
            elif symbol == arcade.key.DOWN:
                self.player_2.direction = -1

    def on_key_release(self, symbol, modifiers):
        """Реакция на отпускание клавиш."""
        if symbol == arcade.key.W:
            self.player_1.direction = 0
        elif symbol == arcade.key.S:
            self.player_1.direction = 0

        if symbol == arcade.key.UP:
            self.player_2.direction = 0
        elif symbol == arcade.key.DOWN:
            self.player_2.direction = 0

    def on_update(self, delta_time):
        """Обновление игровых объектов."""
        for player in self.sprites:
            player.move()
        self.check_goal()
        self.ball.collide_top_bottom()
        self.collide_ball_players()
        self.players.update(delta_time, self.ball.center_y)

    def check_goal(self) -> None:
        """Проверяет забитые голы."""
        if self.ball.right > self.width:
            new_score = int(self.score_p1.text) + 1
            self.score_p1.text = str(new_score)
            arcade.play_sound(self.ball.sounds["score"])
            self.ball.reset()
        elif self.ball.left < 0:
            new_score = int(self.score_p2.text) + 1
            self.score_p2.text = str(new_score)
            arcade.play_sound(self.ball.sounds["score"])
            self.ball.reset()

    def collide_ball_players(self):
        """Столкновения мяча с игроками."""
        # TODO: не проверять коллизию мяча с мячом
        if arcade.check_for_collision_with_list(self.ball, self.sprites):
            self.ball.vel_x *= -1
            arcade.play_sound(self.ball.sounds["collide"])
            # TODO: после вернуть мяч на поверхность ракетки

    def on_draw(self):
        """Отрисовка игровых объектов на окне."""
        self.clear()
        self.draw_dash_lines()
        self.sprites.draw()
        self.score_p1.draw()
        self.score_p2.draw()

    def draw_dash_lines(self) -> None:
        """Рисует пунктирную линию снизу вверх."""
        lines = 30
        line_len = self.height // lines

        start_y = 0
        stop_y = line_len
        for i in range(lines):
            arcade.draw_line(self.width // 2, start_y, self.width // 2, stop_y, arcade.color.WHITE, line_width=10)
            start_y += line_len * 2
            stop_y += line_len * 2


window = arcade.Window(title="Pong", fullscreen=True)
view = MenuView()
window.show_view(view)
arcade.run()
