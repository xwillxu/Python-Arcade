"""
Angry birds(Remake) Tilemap version
"""

"""Instrutions:

1: Click to launch a Angry Bird
2: Take down the pigs with birds
3: Random Bird Launcher
4: Can only launch 5 birds
5: Randomise the box steps
6: Have Fun
7: Made With Tilemap(Inprogress)

"""
# Imports


# Screen setup
import arcade
import random
import math
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Angry Birds"

SCALE = 0.5
BULLET_SPEED = 30
TILE_SCALING = 0.5


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        pass

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        pass

    def on_update(self, delta_time):
        """Update"""

        pass

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        pass


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
