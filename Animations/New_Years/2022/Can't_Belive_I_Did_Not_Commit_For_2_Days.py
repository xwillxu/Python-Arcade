"""Can't Belive i did not commit for 2 days"""

from Animations.Some_Random_Animation import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
import arcade


class Animation(arcade.Window):
    """Animation"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT)

        self.animation_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.SUNSET)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.animation_list.draw()

    def on_update(self, delta_time):
        """Update"""

        self.animation_list.update()


if __name__ == "__main__":
    window = Animation()
    window.setup()
    arcade.run()
