# Deeeep.io Remake

"""
Instrutions:
1. Point to where you want to go so that you will move
2. Kill the AI 
3. If you get killed start again
4. Only 1 skin to try out :(
5. Avoid being hit to heal
6. Defeat the AI
7. Have Fun"""

import arcade
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Deeeep.io 1v1 Remake"

TINY_SCALE = 0.7
SCALE = 0.4
SUPER_SCALE = 0.2


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self):
        """Setup"""

        self.set_fullscreen(not self.fullscreen)

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        self.speed = 5

        self.player = arcade.Sprite("images/Tiger_Shark.png", SCALE)
        self.player.center_x = 600
        self.player.center_y = 400
        self.player.change_x = 0
        self.player.change_y = 0

        self.boost_timer = 0

        self.boost_timer_start = False

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called whenever the mouse button is clicked. """

        self.player_move(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """Mouse Release"""

        self.boost_timer_start = True

    def on_key_press(self, symbol: int, modifiers: int):
        if arcade.key.SPACE:
            self.set_fullscreen(not self.fullscreen)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.player.draw()

    def player_move(self, x, y):
        """Player Move"""

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - self.player.center_x
        y_diff = dest_y - self.player.center_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        self.player.angle = math.degrees(angle) - 90

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.player.change_x = math.cos(angle) * self.speed
        self.player.change_y = math.sin(angle) * self.speed
        # print(f"Bullet change x: {bullet.change_x:.2f}")
        # print(f"Bullet change y: {bullet.change_y:.2f}")

    def on_update(self, delta_time):
        """Update"""

        self.player.update()

        if self.boost_timer_start == True:
            self.boost_timer += 0.01

        if self.boost_timer >= 10:
            self.boost_timer_start = False
            self.boost_timer = 0

        if self.boost_timer > 0:
            self.speed = 10
        else:
            self.speed = 5


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
