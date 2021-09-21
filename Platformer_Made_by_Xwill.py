# Platformer

import arcade

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
SCREEN_TITLE = 'Platformer'


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        '''Setup for platformer'''

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_update(self, delta_time: float):
        '''updates everything'''

    def on_draw(self):
        '''Draws everything'''

        arcade.start_render()

        arcade.draw_rectangle_filled(
            800, 0, 1650, 800, arcade.color.EARTH_YELLOW)


if __name__ == '__main__':
    app = Game()
    arcade.run()
