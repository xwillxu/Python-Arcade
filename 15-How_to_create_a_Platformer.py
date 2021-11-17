# How To Create A Platformer

# Import arcade
import arcade

# Create Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Platformer Tutorial'

SCALE = 0.8

# Create Clas


class Game(arcade.Window):
    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.EMERALD)

        self.enemy_list = arcade.SpriteList()

    def enemy(self, delta_time: float):
        """Enemy Sprite"""

        enemy = arcade.Sprite("arcade/arcade/resources/images/enemies/saw.png")

        enemy.center_x = 600
        enemy.center_y = 400

        self.enemy_list.append(enemy)

    def setup(self):
        """Setup"""

        # setup player
        self.player = arcade.Sprite(
            "arcade/arcade/resources/images/animated_characters/female_adventurer/femaleAdventurer_idle.png", SCALE)

        self.player.center_x = 600
        self.player.center_y = 400

        self.player.change_x = 0
        self.player.change_y = 0
        # Music
        self.background_music = arcade.load_sound(
            "RealPython/materials/arcade-a-primer/sounds/Apoxode_-_Electric_1.wav")

        self.play_music(0)

    def play_music(self, delta_time: float):
        arcade.play_sound(self.background_music)

    def on_key_press(self, key, modifiers):
        """On Key Press"""

        if key == arcade.key.UP:
            self.player.change_y = 7
        if key == arcade.key.DOWN:
            self.player.change_y = -7
        if key == arcade.key.RIGHT:
            self.player.change_x = 7
        if key == arcade.key.LEFT:
            self.player.change_x = -7

    def on_key_release(self, key, modifiers):
        """On Key Release"""
        if key == arcade.key.UP:
            self.player.change_y = 0
        if key == arcade.key.DOWN:
            self.player.change_y = 0
        if key == arcade.key.RIGHT:
            self.player.change_x = 0
        if key == arcade.key.LEFT:
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        """On Update"""

        self.player.update()

        for sprite in self.enemy_list:
            sprite.center_x = sprite.center_x + sprite.change_x * delta_time
            sprite.center_y = sprite.center_y + sprite.change_y * delta_time

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        """On Draw"""
        arcade.start_render()
        # Draw Sprites
        self.player.draw()
        self.enemy_list.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
