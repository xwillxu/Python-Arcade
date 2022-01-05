# Back To School Animation

import arcade

from Happy_New_Years import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


class Animation(arcade.Window):
    """Animation"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.SpriteList = arcade.SpriteList()

    def setup(self):
        """setup"""

        arcade.set_background_color(arcade.color.SKY_BLUE)

        house = arcade.Sprite("images/House.png")

        house.center_x = 600
        house.center_y = 310

        self.SpriteList.append(house)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.SpriteList.draw()

        school_text = "Back To School 2022!(After Winter Break) "

        arcade.draw_text(
            school_text,
            100,
            650,
            arcade.csscolor.BLACK,
            25,
        )

        school_text2 = "Well when we got back it was online school!"
        arcade.draw_text(
            school_text2,
            100,
            600,
            arcade.csscolor.BLACK,
            25,
        )

        school_text3 = "Well I Hope Everyone is Having Fun!"
        arcade.draw_text(
            school_text3,
            100,
            550,
            arcade.csscolor.BLACK,
            25,
        )

        school_text4 = "Bye Xwill"
        arcade.draw_text(
            school_text4,
            100,
            450,
            arcade.csscolor.BLACK,
            25,
        )

    def on_update(self, delta_time):
        """Update"""

        self.SpriteList.update()


if __name__ == "__main__":
    window = Animation()
    window.setup()
    arcade.run()
