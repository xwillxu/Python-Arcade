# Basic arcade shooter

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Space Shooter"
SCALING = 2.0


class SpaceShooter(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title):
        """Initialize the game
        """
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        self.setup()

    def setup(self):
        """Get the game ready to play
        """

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Set up the player
        self.player = arcade.Sprite(
            "RealPython/materials/arcade-a-primer/images/jet.png", SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        self.all_sprites.draw()


# Main code entry point
if __name__ == "__main__":
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


def add_enemy(self, delta_time: float):
    """Adds a new enemy to the screen

    Arguments:s
        delta_time {float} -- How much time has passed since the last call
    """
    # First, create the new enemy sprite
    enemy = ("RealPython/materials/arcade-a-primer/images/missile.png", SCALING)

    # Set its position to a random height and off screen right
    enemy.left = random.randint(self.width, self.width + 80)
    enemy.top = random.randint(10, self.height - 10)

    # Spawn a new enemy every 0.25 seconds
    arcade.schedule(self.add_enemy, 0.25)

    # Spawn a new cloud every second
    arcade.schedule(self.add_cloud, 1.0)

    # Set its speed to a random speed heading left
    enemy.velocity = (random.randint(-20, -5), 0)

    # Add it to the enemies list
    self.enemies_list.append(enemy)
    self.all_sprites.append(enemy)
