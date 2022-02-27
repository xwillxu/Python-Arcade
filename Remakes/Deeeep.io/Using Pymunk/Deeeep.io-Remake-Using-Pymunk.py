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

# Classes


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
        animal_index = random.randint(14, 14)
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
