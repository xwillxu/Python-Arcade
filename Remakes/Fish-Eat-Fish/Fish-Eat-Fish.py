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
    "Anglerfish",
    "Atlantic_Torpedo",
    "Penguin",
    "Giant_Squid",
    "Moray_Eel",
    "Cuddlefish",
    "Marlin",
    "Walrus",
    "Orca",
    "Crocodile",
    "Sawfish",
    "Shark",
    "Giant_Pacific_Octopus",
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

        # Lists
        self.enemy_list = arcade.SpriteList()

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

        # Schedule The Enemys:
        # Coming From The Right Side
        arcade.schedule(self.Enemys_Right, random.randint(5, 25) / 10)

        # Coming From The Left Side
        arcade.schedule(self.Enemys_Left, random.randint(5, 25) / 10)

    def Enemys_Right(self, delta_time):
        """Enemys"""

        # Enemy Id
        enemy_id = random.randint(0, 18)

        # Enemy Name
        enemy_name = enemy_name_list[enemy_id]

        # The Enemy
        enemy = arcade.Sprite(
            f"images/Fish Eat Fish/{enemy_id}_{enemy_name}.webp", 0.3, flipped_diagonally=True)

        # Center X
        enemy.center_x = 1200

        # Center Y
        enemy.center_y = random.randint(100, 1000)
        enemy.change_x = -random.randint(7, 25) / 10
        self.enemy_list.append(enemy)

    def Enemys_Left(self, delta_time):
        """Enemys"""

        enemy_id = random.randint(0, 18)

        animal_name = enemy_name_list[enemy_id]

        enemy = arcade.Sprite(
            f"images/Fish Eat Fish/{enemy_id}_{animal_name}.webp", 0.3, flipped_diagonally=True, flipped_horizontally=True)

        enemy.center_x = 0
        enemy.center_y = random.randint(100, 1000)
        enemy.change_x = random.randint(7, 20) / 10

        self.enemy_list.append(enemy)

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
        self.enemy_list.draw()

    def on_update(self, delta_time):
        """Update"""

        self.player.update()
        self.enemy_list.update()

        # If The PLayer Collides With The Enemy
        for enemy in self.enemy_list:
            if self.player.collides_with_sprite(enemy):
                enemy.remove_from_sprite_lists()
                # Scaling
                self.scale_plus_count += 1
                if self.scale_plus_count % 10 == 0:
                    self.player.scale += 0.1

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
