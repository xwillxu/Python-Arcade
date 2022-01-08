# Dodge The Flame

import random
import arcade
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Dodge the Flame"

SCALE = 0.5
SUPER_SCALE = 0.2
TINY_SCALE = 0.7


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.sprite_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.score = 0

        self.frame_count = 1

        self.player = arcade.Sprite("images/Ice_Cube.png", SUPER_SCALE)

        self.player.center_x = 600
        self.player.center_y = 200

        self.player.change_x = 0

        arcade.schedule(self.flame, 0.15)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.player.draw()
        self.sprite_list.draw()

        score = f"Score: {self.score}"
        arcade.draw_text(
            score,
            100,
            650,
            arcade.csscolor.BLACK,
            25,
        )

    def flame(self, delta_time):
        """Flame"""

        Fire = arcade.Sprite("images/Fire.png", SUPER_SCALE)

        Fire.center_x = random.randint(0, 1200)
        Fire.center_y = 800

        Fire.change_y = -random.randint(2, 6)

        self.sprite_list.append(Fire)

    def on_update(self, delta_time):
        """Update"""

        self.frame_count += 1

        if self.frame_count % 60 == 0:
            self.score += 1

        self.player.update()
        self.sprite_list.update()

        #  Did we hit anything? If so, end the game
        if self.player.collides_with_list(self.sprite_list):
            arcade.close_window()

        # Keep the player on screen
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.left < 0:
            self.player.left = 0

    def on_key_press(self, key, modifiers):
        """On Key Press"""

        if key == arcade.key.RIGHT:
            self.player.change_x = 5
        if key == arcade.key.LEFT:
            self.player.change_x = -5

    def on_key_release(self, key, modifiers):
        """On Key Release"""
        if key == arcade.key.RIGHT:
            self.player.change_x = 0
        if key == arcade.key.LEFT:
            self.player.change_x = 0


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
