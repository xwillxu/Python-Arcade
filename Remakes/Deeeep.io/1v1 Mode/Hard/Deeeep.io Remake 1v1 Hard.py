# Deeeep.io Remake

"""
Instrutions:
1. Point to where you want to go so that you will move
2. Kill the AI 
3. Try out new skins
4. If you get killed start again
5. Don't like your skin? Click on the pause button,
then click on skins, and change into a new skin.(You
will not heal.)
6. Avoid being hit to heal
7. Choose a form of AI to play against.
8. Have Fun(As Always)"""

import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Deeeep.io 1v1 Remake"


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

    def on_update(self, delta_time):
        """Update"""


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
