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

enemy_list_new = [
    {
        'name': "Piranha",
        'scale': 0.2,
    },
    {
        "name": "Ray",
        "scale": 0.2,
    },
    {
        "name": "Bobbit_Worm",
        "scale": 0.2,
    },
    {
        "name": "Clownfish",
        "scale": 0.2,
    },
    {
        "name": "Jellyfish",
        "scale": 0.3,
    },
    {
        "name": "Sunfish",
        "scale": 0.35,
    },
    {
        "name": "Anglerfish",
        "scale": 0.35,
    },
    {
        "name": "Atlantic_Torpedo",
        "scale": 0.35,
    },
    {
        "name": "Penguin",
        "scale": 0.45,
    },
    {
        "name": "Giant_Squid",
        "scale": 0.4,
    },
    {
        "name": "Moray_Eel",
        "scale": 1.1,
    },

    {
        "name": "Cuddlefish",
        "scale": 1.2,
    },

    {
        "name": "Marlin",
        "scale": 0.9,
    },

    {
        "name": "Walrus",
        "scale": 0.9,
    },

    {
        "name": "Orca",
        "scale": 1.7,
    },

    {
        "name": "Crocodile",
        "scale": 1.6,
    },

    {
        "name": "Sawfish",
        "scale": 1.3,
    },

    {
        "name": "Shark",
        "scale": 1.7,
    },
    {
        "name": "Giant_Pacific_Octopus",
        "scale": 4.5,
    },



]

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


class Player(arcade.Sprite):
    """Player"""

    def __init__(self):
        """Init"""
        super().__init__()

        # Scale And Texture
        self.scale = 0.0475
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
        """Update"""

        # Update Stuff
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

        # Score
        self.score = 300

        # Frame Count
        self.frame_count = 0

        # Schedule The Enemys:
        # Coming From The Right Side
        arcade.schedule(self.Enemys_Right, random.randint(5, 15) / 10)

        # Coming From The Left Side
        arcade.schedule(self.Enemys_Left, random.randint(5, 15) / 10)

    def Enemys_Right(self, delta_time):
        """Enemys"""

        # Enemy Id
        enemy_id = random.randint(0, 18)

        # Enemy Name
        enemy_object = enemy_list_new[enemy_id]

        # The Enemy
        enemy = arcade.Sprite(
            f"images/Fish Eat Fish/{enemy_id}_{enemy_object['name']}.webp", enemy_object['scale'], flipped_diagonally=True)

        # Enemy Size
        enemy_size = enemy.width * enemy.height
        # Player Size
        player_size = self.player.width * self.player.height
        # Method
        if enemy_size / 2 > player_size or enemy_size * 3 < player_size:
            return

        # Center X
        enemy.center_x = 1200
        # Center Y
        enemy.center_y = random.randint(100, 1000)
        # Change X
        enemy.change_x = -random.randint(7, 25) / 10

        # Score
        enemy.score = 5 + enemy_id

        # Scale Added If Eaten
        enemy.scale_plus = 0.0005 * enemy.score

        # Add To List
        self.enemy_list.append(enemy)

    def Enemys_Left(self, delta_time):
        """Enemys"""

        # Enemy Id
        enemy_id = random.randint(0, 18)

        # Enemy Name
        enemy_object = enemy_list_new[enemy_id]

        self.enemy_name = enemy_id

        # The Enemy
        enemy = arcade.Sprite(
            f"images/Fish Eat Fish/{enemy_id}_{enemy_object['name']}.webp", enemy_object['scale'], flipped_diagonally=True, flipped_horizontally=True)

        # Enemy Size
        enemy_size = enemy.width * enemy.height
        # Player Size
        player_size = self.player.width * self.player.height
        # Method
        if enemy_size / 2 > player_size or enemy_size * 4 < player_size:
            return

        # Center X
        enemy.center_x = 0
        # Center Y
        enemy.center_y = random.randint(100, 1000)
        # Change X
        enemy.change_x = random.randint(7, 25) / 10

        # Score
        enemy.score = 5 + enemy_id

        # Scale Added If Eaten
        enemy.scale_plus = 0.0005 * enemy.score

        # Add To List
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

        # Draw Your Score
        output = f"Your Score: {self.score}"
        arcade.draw_text(output, 10, 770, arcade.color.SUNSET, 19)

    def on_update(self, delta_time):
        """Update"""

        # Update Everything
        self.player.update()
        self.enemy_list.update()

        # Change The Frame Count
        self.frame_count += 1

        # When The Game Starts For The First Five Seconds The Score Will Go Up By One Hundred Points
        if not self.score >= 400:
            if self.frame_count % 5 == 0:
                self.score += 1
                self.player.scale += 0.0005

        # If The Player Collides With The Enemy
        for enemy in self.enemy_list:
            if self.player.collides_with_sprite(enemy):
                # For Every Animal Check If You Can Eat It Or Not
                # Player Size
                player_size = self.player.width * self.player.height
                # Enemy Size
                enemy_size = enemy.width * enemy.height
                # What Happens If You Can Eat The Enemy
                if player_size > enemy_size:
                    self.score += enemy.score
                    self.player.scale += enemy.scale_plus
                    enemy.remove_from_sprite_lists()
                # If Not
                else:
                    arcade.close_window()

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
