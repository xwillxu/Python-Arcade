"""

This Is My Deeeep.io Version Using Pymunk 
So That The Collision And Stuff Like That Is Not Crappy.

"""

# Import Librarys And Modules
import arcade
import pymunk
import random
import math

# Screen Properties
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Deeeep.io(Remake) Using Pymunk"

# HealthBar Setup
HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 10
HEALTHBAR_OFFSET_Y = 50

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


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x,
                         center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape


class CircleSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class BoxSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename, width, height):
        super().__init__(pymunk_shape, filename)
        self.width = width
        self.height = height


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Add Lists

        self.box_list: arcade.SpriteList[PhysicsSprite] = arcade.SpriteList()
        self.static_lines = []

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        # Set Random Player Animal At The Start Of The Game
        animal_index = random.randint(1, 15)
        animal_name = animal_name_list[animal_index - 1]
        animal_attributes = animals[animal_name]

        # Player
        self.player = arcade.Sprite(f"images/Deeeep.io/{animal_name}")

        # Pymunk Setup
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, -900.0)

        # Create Floor
        floor_height = 80
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Segment(body, [0, floor_height], [
                               SCREEN_WIDTH, floor_height], 0.0)
        shape.friction = 10
        self.space.add(shape, body)
        self.static_lines.append(shape)

    def on_key_press(self, key, modifiers):
        """Key Press"""

        pass

    def on_key_release(self, key, modifiers):
        """Key Press"""

        pass

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        pass

    def on_update(self, delta_time):
        """Update"""

        pass


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
