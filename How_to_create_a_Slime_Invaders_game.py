# Slime Invaders

# Imports
import arcade

# Screen varibles
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Slime Invaders"

# Classes


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """Setup"""

        self.player = arcade.Sprite("images/player_2/player_stand.png")
        self.player.center_x = 600
        self.player.center_y = 400
        self.player.change_x = 0
        self.player.change_y = 0

    def on_key_press(self, key, modifiers):
        """Key Press"""

        if key == arcade.key.LEFT:
            self.player.change_x += -5
        if key == arcade.key.RIGHT:
            self.player.change_x += 5

    def on_key_release(self, key, modifiers):
        """Key Release"""
        if key == arcade.key.LEFT:
            self.player.change_x == 0
        if key == arcade.key.RIGHT:
            self.player.change_x == 0

    def on_update(self, delta_time: float):
        """Update"""

        self.player.update()

    def on_draw(self):
        """Draw window"""

        arcade.start_render()

        self.player.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
