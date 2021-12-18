"""
Angry birds(Remake)
"""
# Imports
import arcade
import pymunk
import math

# Screen setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Angry Birds"

SCALE = 0.5

# Classes


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x,
                         center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape


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

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        # Player Setup
        self.player = arcade.Sprite("images/bird.png", SCALE)

        # Player Start X and Y
        self.player.center_x = 200
        self.player.center_y = 200

        # Player's change X and Y
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

        for row in range(10):
            for column in range(2):
                size = 32
                mass = 1.0
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

    # Sprites

    def angry_bird_launch(self, x, y):
        """Angry Bird Launch"""

        angry_bird = arcade.Sprite("images/bird.png")

    def on_mouse_press(self, x, y, button, modifiers):
        """Mouse Press"""

        if button == arcade.MOUSE_BUTTON_LEFT or arcade.MOUSE_BUTTON_RIGHT:
            self.angry_bird_launch(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """Mouse Release"""

        pass

    def on_update(self, delta_time):
        """Update"""

        # Update Stuff
        self.player.update()

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        # Draw Stuff
        self.player.draw()
        self.box_list.draw()

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
