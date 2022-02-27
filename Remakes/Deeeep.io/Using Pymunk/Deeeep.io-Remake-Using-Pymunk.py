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
        self.player = Health_Sprite(
            f"images/Deeeep.io/{animal_name}.png", animal_attributes["scale"], max_health=animal_attributes["health"])
        self.player.center_x = random.randint(10, 1190)
        self.player.center_y = random.randint(10, 790)
        self.player.change_x = 0
        self.player.change_y = 0

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

    def player_movement(self, x, y):
        """Player Movement"""

        # Position the bullet at the player's current location
        start_x = self.player.center_x
        start_y = self.player.center_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # By calculating the distance between mouse click and the player sprite
        velocity = (x_diff * x_diff + y_diff * y_diff) / 100

        # you can only have 1000 max
        if velocity > 400:
            velocity = 400

        velocity_x = math.cos(angle) * velocity
        velocity_y = math.sin(angle) * velocity

        # With right mouse button, shoot a heavy coin fast.
        mass = 0.5
        radius = 20
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)

        # set the physics object starting place
        body.position = start_x, start_y  # the same as set a spirte center_x and center_y

        # set the physics object staring speed, just like you setting change_x and change_y
        body.velocity = velocity_x, velocity_y

        shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
        shape.friction = 0.3
        self.space.add(body, shape)

        # Set Random Player Animal At The Start Of The Game
        animal_index = random.randint(1, 15)
        animal_name = animal_name_list[animal_index - 1]
        animal_attributes = animals[animal_name]

        # Player
        self.player = BoxSprite(
            f"images/Deeeep.io/{animal_name}", animal_attributes["scale"])
        self.player.center_x = random.randint(10, 1190)
        self.player.center_y = random.randint(10, 790)

    def on_mouse_motion(self, x, y, dx, dy):
        """Mouse Motion"""

        self.player_movement(x, y)

    def on_key_press(self, key, modifiers):
        """Key Press"""

        pass

    def on_key_release(self, key, modifiers):
        """Key Press"""

        pass

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.player.draw()

    def on_update(self, delta_time):
        """Update"""

        pass


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
