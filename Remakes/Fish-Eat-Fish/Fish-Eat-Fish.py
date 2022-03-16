# Import Librarys And Modules
import arcade

# Screen Properties
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Fish Eat Fish"

# The Game Class


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        pass

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        self.player = arcade.Sprite(
            "images/Fish Eat Fish/You.png", 0.15)
        self.player.center_x = 600
        self.player.center_y = 400
        self.player.change_x = 0
        self.player.change_y = 0

    def on_key_press(self, key, modifiers):
        """Key Press"""

        if key == arcade.key.UP:
            self.player.change_y += 5
        elif key == arcade.key.DOWN:
            self.player.change_y += -5
        elif key == arcade.key.LEFT:
            self.player.change_x += -5
        elif key == arcade.key.RIGHT:
            self.player.change_x += 5

    def on_key_release(self, key, modifiers):
        """Key Press"""

        if key == arcade.key.UP:
            self.player.change_y = 0
        elif key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.player.draw()

    def on_update(self, delta_time):
        """Update"""

        self.player.update()

        # if self.player.change_x > 0:
        #     self.player = arcade.Sprite(
        #         "images/Fish Eat Fish/You.png", 0.2, 0, 0, 0, 0, 0, 0, 1, 1, True)
        #     self.player.center_x = 600
        #     self.player.center_y = 400

        # else:
        #     self.player = arcade.Sprite(
        #         "images/Fish Eat Fish/You.png", 0.2, 0, 0, 0, 0, 0, 0, 1, 1, False)
        #     self.player.center_x = 600
        #     self.player.center_y = 400


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
