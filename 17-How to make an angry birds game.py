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

SCALE = 0.5

# Classes


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Add Lists

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        # Player Setup
        self.player = arcade.Sprite("images/bird.png", SCALE, 0, 0, 0,
                                    0, 0, 0, 1, 1, False, False, False, "Simple", 4.5, None, 0)

        # Player Start X and Y
        self.player.center_x = 600
        self.player.center_y = 400

        # Player's change X and Y
        self.player.change_x = 0
        self.player.change_y = 0

    def on_key_press(self, key, modifiers):
        """Key Press"""

        pass

    def on_key_release(self, key, modifiers):
        """Key Release"""

        pass

    def on_update(self, delta_time):
        """Update"""

        # Update Stuff
        self.player.update()

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        # Draw Stuff
        self.player.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
