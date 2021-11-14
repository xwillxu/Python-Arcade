# How To Create A Platformer

# Import arcade
import arcade
from arcade.application import Window

# Create Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Platformer Tutorial'

SCALE = 1

# Create Class


class Game(arcade.Window):
    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        """Setup"""

        # setup player
        self.player = arcade.Sprite(
            "arcade/arcade/resources/images/animated_characters/female_adventurer/femaleAdventurer_idle.png", SCALE)

        self.player.center_x = 600
        self.player.center_y = 400

    def on_draw(self):
        """On Draw"""
        arcade.start_render()

        self.player.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
