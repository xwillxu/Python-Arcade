# Import Librarys And Modules
import arcade
import random

# Screen Properties
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Fish Eat Fish"

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

enemy_name_list = [
    "Piranha",
    "Ray",
    "Bobbit_Worm",
    "Clownfish",
    "Jellyfish",
    "Sunfish",
    "",
    "",
    "",
]

enemys = {

}


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.scale = 0.15
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture("images/Fish Eat Fish/You.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/Fish Eat Fish/You.png",
                                      flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

# The Game Class


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        pass

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        # Setup Player
        self.player = Player()
        # X
        self.player.center_x = 600
        self.player.change_x = 0
        # Y
        self.player.center_y = 400
        self.player.change_y = 0

    def Enemys(self):
        """Enemys"""

        enemy_id = random.randint(4, 17) * 100

        animal_name = enemy_name_list[enemy_id - 1]

        enemy_attributes = enemys[animal_name]

        enemy = arcade.Sprite("images/Fish Eat Fish/")

    def on_key_press(self, key, modifiers):
        """Key Press"""

        # Up
        if key == arcade.key.UP:
            self.player.change_y += 5
        # Down
        elif key == arcade.key.DOWN:
            self.player.change_y += -5
        # Left
        elif key == arcade.key.LEFT:
            self.player.change_x += -5
        # Right
        elif key == arcade.key.RIGHT:
            self.player.change_x += 5

    def on_key_release(self, key, modifiers):
        """Key Press"""

        # Up
        if key == arcade.key.UP:
            self.player.change_y = 0
        # Down
        elif key == arcade.key.DOWN:
            self.player.change_y = 0
        # Left
        elif key == arcade.key.LEFT:
            self.player.change_x = 0
        # Right
        elif key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.player.draw()

    def on_update(self, delta_time):
        """Update"""

        self.player.update()

        # Keep The Player From Going Off The Screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
