"""

This Is My Deeeep.io Version Using Pymunk 
So That The Collision And Stuff Like That Is Not Crappy.

"""

# Import Librarys And Modules
import arcade
import random
import math
from arcade.pymunk_physics_engine import PymunkPhysicsEngine
from Pymunk_Helping_Code import follow_sprite

# Screen Properties
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Deeeep.io(Remake) Using Pymunk"

# Healthbar Setup
HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 10
HEALTHBAR_OFFSET_Y = 50

# Different Scales
TINY_SCALE = 0.7
SCALE = 0.4
SUPER_SCALE = 0.2

# Animal Dictionary
animal_name_list = [
    'Alligator_Snapping_Turtle',
    'Blue_Whale',
    'Elephant_Seal',
    'Goblin_Shark',
    'Humpback_Whale',
    'Leatherback_Turtle',
    'Manta_Ray',
    'Marlin',
    'Orca',
    'Polar_Bear',
    'Sleeper_Shark',
    'Sperm_Whale',
    'Sunfish',
    'Tiger_Shark',
    'Walrus', ]

animals = {

    # 1
    'Alligator_Snapping_Turtle': {
        'health': 800,
        'speed': 90,
        'damage': 140,
        'scale': 0.5
    },
    # 2
    'Blue_Whale': {
        'health': 1500,
        'speed': 90,
        'damage': 120,
        'scale': 0.7
    },

    # 3
    "Elephant_Seal": {
        'health': 1000,
        'speed': 90,
        'damage': 120,
        'scale': 0.5
    },
    # 4
    'Goblin_Shark': {
        'health': 750,
        'speed': 100,
        'damage': 140,
        'scale': 0.4
    },
    # 5
    'Humpback_Whale': {
        'health': 1200,
        'speed': 90,
        'damage': 100,
        'scale': 0.55
    },
    # 6
    'Leatherback_Turtle': {
        'health': 900,
        'speed': 95,
        'damage': 130,
        'scale': 0.4
    },

    # 7
    'Manta_Ray': {
        'health': 1000,
        'speed': 100,
        'damage': 120,
        'scale': 0.4
    },
    # 8
    'Marlin': {
        'health': 700,
        'speed': 125,
        'damage': 100,
        'scale': 0.3
    },


    # 9
    'Orca': {
        'health': 900,
        'speed': 100,
        'damage': 160,
        'scale': 0.4
    },
    # 10
    'Polar_Bear': {
        'health': 900,
        'speed': 100,
        'damage': 160,
        'scale': 0.4
    },
    # 11
    'Sleeper_Shark': {
        'health': 1000,
        'speed': 80,
        'damage': 160,
        'scale': 0.4
    },
    # 12
    'Sperm_Whale': {
        'health': 1200,
        'speed': 85,
        'damage': 160,
        'scale': 0.55
    },

    # 13
    'Sunfish': {
        'health': 900,
        'speed': 100,
        'damage': 140,
        'scale': 0.4
    },

    # 14
    'Tiger_Shark': {
        'health': 800,
        'speed': 100,
        'damage': 160,
        'scale': 0.4
    },

    # 15
    'Walrus': {
        'health': 900,
        'speed': 90,
        'damage': 140,
        'scale': 0.3
    },


}

# Classes


class Health_Sprite(arcade.Sprite):
    '''Health Sprite'''

    def __init__(self, image, scale, max_health):
        super().__init__(image, scale)

        self.max_health = max_health
        self.cur_health = max_health

    def draw_health_bar(self):
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=HEALTHBAR_HEIGHT,
                                         color=arcade.color.BLACK)

        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Add Lists
        self.orb_list = None
        self.orb_list2 = None
        self.fish_list = None

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        # Set Random Player Animal At The Start Of The Game
        animal_index = random.randint(1, 15)
        animal_name = animal_name_list[animal_index - 1]
        animal_attributes = animals[animal_name]

        # Player
        self.player = Health_Sprite(
            f"images/Deeeep.io/{animal_name}.png", animal_attributes["scale"], max_health=animal_attributes["health"])
        self.player.center_x = random.randint(10, 1190)
        self.player.center_y = random.randint(10, 790)
        self.player.change_x = 0
        self.player.change_y = 0

        # Speed
        self.speed = animal_attributes['speed'] / 9 / 2

        # Food Setup
        self.orb_list = arcade.SpriteList()
        self.orb_list2 = arcade.SpriteList()
        self.fish_list = arcade.SpriteList()

        # Spawn Food
        for i in range(50):
            self.GreenOrb()
        for i in range(50):
            self.BlueOrb()
        for i in range(5):
            self.fish()

    def player_movement(self, x, y):
        """Player Movement"""

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

    def GreenOrb(self):
        """Orb"""

        # Green Orb Random Spawn Position
        center_x = random.randint(10, 1890)
        center_y = random.randint(10, 1040)

        # Green Orb Setup
        orb = arcade.Sprite("images/Orb.png", SCALE / 4)

        orb.center_x = center_x
        orb.center_y = center_y

        # Add To List To Draw
        self.orb_list.append(orb)

    def BlueOrb(self):
        """Orb"""

        # Blue Orb Random Spawn Position
        center_x = random.randint(10, 1890)
        center_y = random.randint(10, 1040)

        # Blue Orb Setup
        orb = arcade.Sprite("images/Orb2.png", SCALE / 4)

        orb.center_x = center_x
        orb.center_y = center_y

        # Add To List To Draw
        self.orb_list2.append(orb)

    def fish(self):
        """fish"""

        # Fish Setup
        fish = arcade.Sprite("images/Sardine.png", SUPER_SCALE/4)

        fish.center_x = random.randint(10, 1890)
        fish.center_y = random.randint(10, 1040)

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = random.randint(10, 1890)
        dest_y = random.randint(10, 1040)

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - fish.center_x
        y_diff = dest_y - fish.center_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        fish.angle = math.degrees(angle) - 90

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        fish.change_x = math.cos(angle) * 4.5
        fish.change_y = math.sin(angle) * 4.5

        # Add the bullet to the appropriate lists
        self.fish_list.append(fish)

    def on_mouse_motion(self, x, y, dx, dy):
        """Mouse Motion"""

        self.player_movement(x, y)

    def on_key_press(self, key, modifiers):
        """Key Press"""

        pass

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        # Draw The Player
        self.player.draw()

        # Draw Lists
        self.orb_list.draw()
        self.orb_list2.draw()
        self.fish_list.draw()

    def on_update(self, delta_time):
        """Update"""

        # Update Everything
        self.player.update()
        self.orb_list.update()
        self.orb_list2.update()
        self.fish_list.update()

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
