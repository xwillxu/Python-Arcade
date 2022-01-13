"""Can't Belive i did not commit for 2 days"""

import arcade
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Can't Belive i did not commit for 2 days"


class Animation(arcade.Window):
    """Animation"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.animation_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.animation_list.draw()

        arcadetext = "Sorry that i did not commit for the last 2 days. I was busy."
        arcade.draw_text(arcadetext, 150, 500, arcade.color.SUNGLOW, 25)
        arcadetext2 = "I hope that never happens again."
        arcade.draw_text(arcadetext2, 150, 450, arcade.color.SUNGLOW, 25)
        arcadetext3 = "Xwill Xu"
        arcade.draw_text(arcadetext3, 150, 350, arcade.color.SUNGLOW, 25)

    def on_update(self, delta_time):
        """Update"""

        self.animation_list.update()


if __name__ == "__main__":
    window = Animation()
    window.setup()
    arcade.run()
