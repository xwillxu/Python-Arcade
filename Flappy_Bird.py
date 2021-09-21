# Flappy bird

import arcade
import random


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Flappy Bird"


class Game(arcade.Window):
    '''Game window for flappy bird'''

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.pipe_lists = arcade.SpriteList()
        self.pipe2_lists = arcade.SpriteList()
        self.flappy_bird = arcade.Sprite(
            "images/Flappy_bird.png", 0.13
        )

        self.score = 0

        self.flappy_bird.center_x = 300
        self.flappy_bird.center_y = 500

        self.flappy_bird.change_y = 0

        self.pipes(0)

        arcade.schedule(self.pipes, 2.0)

        arcade.schedule(self.score_change, 2.0)

    def score_change(self, delta_time: float):
        self.score += 1

    def pipes(self, delta_time: float):
        pipe = arcade.Sprite("images/pipe.png", 0.35, 0,
                             0, 0, 0, 0, 0, 1, 1, False, True)

        pipe.top = random.randint(1000, 1300)
        pipe.left = 2000

        pipe.velocity = (-200, 0)

        self.pipe_lists.append(pipe)

        pipe_2 = arcade.Sprite("images/pipe.png", 0.35, 0,
                               0, 0, 0, 0, 0, 1, 1, False, False)

        pipe_2.center_x = pipe.center_x
        pipe_2.center_y = pipe.center_y - 800

        pipe_2.velocity = (-200, 0)

        self.pipe2_lists.append(pipe_2)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.flappy_bird.change_y = 9
        if symbol == arcade.key.SPACE:
            self.flappy_bird.change_y = 9

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.flappy_bird.change_y = -8
        if symbol == arcade.key.SPACE:
            self.flappy_bird.change_y = -8

    def on_update(self, delta_time: float):
        self.flappy_bird.center_y = self.flappy_bird.center_y + self.flappy_bird.change_y

        for pipe in self.pipe_lists:
            if self.flappy_bird.collides_with_sprite(pipe):
                arcade.close_window()

        for pipe2 in self.pipe2_lists:
            if self.flappy_bird.collides_with_sprite(pipe2):
                arcade.close_window()

        for sprite in self.pipe_lists:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
        for sprite in self.pipe2_lists:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
        if self.flappy_bird.top > self.height:
            self.flappy_bird.top = self.height
        if self.flappy_bird.bottom < 0:
            arcade.close_window()

    def on_draw(self):
        ''' Called when needed to draw '''

        arcade.start_render()

        self.flappy_bird.draw()
        self.pipe_lists.draw()
        self.pipe2_lists.draw()

        time_text = f"Score: {self.score:.0f}"
        arcade.draw_text(time_text, 1200, 960, arcade.color.BLACK, 20)


if __name__ == "__main__":
    app = Game()
    arcade.run()
