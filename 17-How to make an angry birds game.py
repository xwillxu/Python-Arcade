"""
Angry birds(Remake)
"""
# Imports
import arcade
import random
import pymunk
import math

# Screen setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Angry Birds"

SCALE = 0.5
BULLET_SPEED = 30

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
    """Game Window"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Add Lists

        self.box_list: arcade.SpriteList[PhysicsSprite] = arcade.SpriteList()
        self.static_lines = []
        self.angry_bird_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        # Player Setup
        self.player = arcade.Sprite("images/ClassicChuck2.png", SCALE)

        # Player Start X and Y
        self.player.center_x = 200
        self.player.center_y = 200

        # Player's change X and Y
        self.player.change_x = 0
        self.player.change_y = 0

        # Angry Bird Count
        self.angry_bird_count = 0

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

        for row in range(random.randint(5, 9)):
            for column in range(1):
                size = 32
                mass = 1.5
                x = 800 + column * 32
                y = (floor_height + size / 2) + row * size
                moment = pymunk.moment_for_box(mass, (size, size))
                body = pymunk.Body(mass, moment)
                body.position = pymunk.Vec2d(x, y)
                shape = pymunk.Poly.create_box(body, (size, size))
                shape.elasticity = 0.2
                shape.friction = 0.9
                self.space.add(body, shape)

                sprite = BoxSprite(
                    shape, ":resources:images/tiles/boxCrate_double.png", width=size, height=size)
                self.box_list.append(sprite)

        for row in range(random.randint(5, 9)):
            for column in range(1):
                size = 32
                mass = 1.5
                x = 840 + column * 32
                y = (floor_height + size / 2) + row * size
                moment = pymunk.moment_for_box(mass, (size, size))
                body = pymunk.Body(mass, moment)
                body.position = pymunk.Vec2d(x, y)
                shape = pymunk.Poly.create_box(body, (size, size))
                shape.elasticity = 0.2
                shape.friction = 0.9
                self.space.add(body, shape)

                sprite = BoxSprite(
                    shape, ":resources:images/tiles/boxCrate_double.png", width=size, height=size)
                self.box_list.append(sprite)

        for row in range(random.randint(5, 9)):
            for column in range(1):
                size = 32
                mass = 1.5
                x = 880 + column * 32
                y = (floor_height + size / 2) + row * size
                moment = pymunk.moment_for_box(mass, (size, size))
                body = pymunk.Body(mass, moment)
                body.position = pymunk.Vec2d(x, y)
                shape = pymunk.Poly.create_box(body, (size, size))
                shape.elasticity = 0.2
                shape.friction = 0.9
                self.space.add(body, shape)

                sprite = BoxSprite(
                    shape, ":resources:images/tiles/boxCrate_double.png", width=size, height=size)
                self.box_list.append(sprite)

        for row in range(1):
            for column in range(3):
                size = 32
                mass = 1.0
                x = 800 + column * 31
                y = (floor_height + size / 2) + row * size + 300
                moment = pymunk.moment_for_box(mass, (size, size))
                body = pymunk.Body(mass, moment)
                body.position = pymunk.Vec2d(x, y)
                shape = pymunk.Poly.create_box(body, (size, size))
                shape.elasticity = 0.2
                shape.friction = 0.9
                self.space.add(body, shape)

                sprite = BoxSprite(
                    shape, "images/pig.png", width=size, height=size)
                self.box_list.append(sprite)

    # Sprites

    def angry_bird_launch(self, x, y):
        """Angry Bird Launch"""

        if self.angry_bird_count < 5:

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
            if velocity > 1000:
                velocity = 1000

            velocity_x = math.cos(angle) * velocity
            velocity_y = math.sin(angle) * velocity

            # With right mouse button, shoot a heavy coin fast.
            mass = 0.7
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

            bird_random = random.randint(1, 3)

            # Create a bullet
            angry_bird = CircleSprite(shape,
                                      f"images/ClassicChuck{bird_random}.png")

            self.angry_bird_count += 1

            # Add the bullet to the appropriate lists
            self.angry_bird_list.append(angry_bird)

    def on_mouse_press(self, x, y, button, modifiers):
        """Mouse Press"""

        self.angry_bird_launch(x, y)

    def on_update(self, delta_time):
        """Update"""

        # Update Stuff
        self.player.update()
        self.box_list.update()
        self.angry_bird_list.update()

        # Update physics
        # Use a constant time step, don't use delta_time
        # See "Game loop / moving time forward"

        self.space.step(1 / 60.0)

        for sprite in self.box_list:
            if sprite.pymunk_shape.body.position.y < 0:
                # Remove balls from physics space
                self.space.remove(sprite.pymunk_shape,
                                  sprite.pymunk_shape.body)
                # Remove balls from physics list
                sprite.remove_from_sprite_lists()

        # Move sprites to where physics objects are
        for sprite in self.box_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

        # Move sprites to where physics objects are
        for sprite in self.angry_bird_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        # Draw Stuff
        self.player.draw()
        self.box_list.draw()
        self.angry_bird_list.draw()

        for line in self.static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcade.draw_line(pv1.x, pv1.y - 48, pv2.x, pv2.y - 48,
                             arcade.color.GREEN_YELLOW, 95)


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
