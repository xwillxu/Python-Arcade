"""
Angry birds(Remake)
"""
# Imports
import arcade
import pymunk

# Screen setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Angry Birds"


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.AERO_BLUE)

    def on_key_press(self, key, modifiers):
        """Key Press"""

        pass

    def on_key_release(self, key, modifiers):
        """Key Release"""

        pass

    def on_update(self, delta_time):
        """Update"""

        pass

    def on_draw(self):
        """Draw"""

        arcade.start_render()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
