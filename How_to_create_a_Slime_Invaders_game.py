# Slime Invaders

# Imports
import arcade

# Screen Varibles
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Slime Invaders"

# Global Varibles
SCALE = 0.5

# Classes


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AMAZON)

        self.shield_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        self.player = arcade.Sprite("images/player_2/player_stand.png", SCALE)
        self.player.center_x = 600
        self.player.center_y = 100
        self.player.change_x = 0
        self.player.change_y = 0

        self.background_music = arcade.load_sound(
            "RealPython/materials/arcade-a-primer/sounds/Apoxode_-_Electric_1.wav")

        self.shield()

        self.music(0)

        arcade.schedule(self.music, 15.5)

    def music(self, delta_time: float):
        """Music"""

        arcade.play_sound(self.background_music)

    def bullet(self):
        """Bullet"""

        player_bullet = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png", SCALE)

    def shield(self):
        """Shield"""

        shield = arcade.Sprite("images/wood1.png", SCALE)

        shield.center_x = 600
        shield.center_y = 200

        self.shield_list.append(shield)

        shield = arcade.Sprite("images/wood1.png", SCALE)

        shield.center_x = 200
        shield.center_y = 200

        self.shield_list.append(shield)

        shield = arcade.Sprite("images/wood1.png", SCALE)

        shield.center_x = 1000
        shield.center_y = 200

        self.shield_list.append(shield)

    def on_key_press(self, key, modifiers):
        """Key Press"""

        if key == arcade.key.LEFT:
            self.player.change_x = -7
        if key == arcade.key.RIGHT:
            self.player.change_x = 7

    def on_key_release(self, key, modifiers):
        """Key Release"""
        if key == arcade.key.LEFT:
            self.player.change_x = 0
        if key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        """Update"""

        self.player.update()

        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        """Draw window"""

        arcade.start_render()

        self.player.draw()
        self.shield_list.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
