# Some Random Animation(Unfinshed Will get back to it.


import arcade
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = " Some Random Animation"


class Animation(arcade.Window):
    """Animation"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_HEIGHT)

        self.animation_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.SUNSET)

        sunset = arcade.Sprite("images/SunsetBackround.jpg")

        sunset.center_x = 600
        sunset.center_y = 400

        self.animation_list.append(sunset)

        sparkle = arcade.Sprite("images/sparkle.png")

        sparkle.center_x = 600
        sparkle.center_y = 300

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
