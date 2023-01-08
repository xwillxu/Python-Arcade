# 2023 Animation

import arcade
import random

from Happy_New_Years import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


class Animation(arcade.Window):
    """Animation"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.background_list = arcade.SpriteList()
        self.snowflake_list = arcade.SpriteList()
        self.new_year_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.LIGHT_SKY_BLUE)

        self.frame_count = 1

        backround = arcade.Sprite("images/2022_Backround.jpg")

        backround.center_x = 600
        backround.center_y = 400

        self.background_list.append(backround)

        New_Year = arcade.Sprite("images/2023-Image.png")

        New_Year.center_x = 600
        New_Year.center_y = 400

        self.new_year_list.append(New_Year)

        self.Jingle_bells = arcade.Sound(
            "sounds/jingle-bells-violin-loop-8645.mp3")

        arcade.schedule(self.JingleBells, 175)

        self.JingleBells(0)

    def JingleBells(self, delta_time):
        """Jingle Bells"""

        arcade.play_sound(self.Jingle_bells)

    def snowflakes(self):
        """Snowflakes"""

        scale = random.randint(8, 11)

        snowflake = arcade.Sprite("images/snowflake.png", scale / 10)

        snowflake.center_x = random.randint(100, 1100)
        snowflake.center_y = 800

        snowflake.change_x = 0
        snowflake.change_y = random.randint(-4, -2)

        self.snowflake_list.append(snowflake)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.background_list.draw()
        self.snowflake_list.draw()
        self.new_year_list.draw()

    def on_update(self, delta_time):
        """Update"""

        self.snowflake_list.update()

        self.frame_count += 1

        if self.frame_count % 5 == 0:
            self.snowflakes()


if __name__ == "__main__":
    window = Animation()
    window.setup()
    arcade.run()
