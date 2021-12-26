"""
Angry birds(Remake) Tilemap version
"""

"""Instrutions:

1: Click to launch a Angry Bird
2: Take down the pigs with birds
3: Random Bird Launcher
4: Can only launch 5 birds
5: Randomise the box steps
6: Have Fun
7: Made With Tilemap
8: Make it with camera
9: Make it like the real Game

"""
# Imports


# Screen setup

import arcade
import random
import math
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Angry Birds"

# Scale
SCALE = 0.5

# Bullet Speed
BULLET_SPEED = 30

# Gravity
GRAVITY = 1500

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0

# Friction between objects
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

# How much force to put on the bullet
BULLET_MOVE_FORCE = 60000

# Mass of the bullet
BULLET_MASS = 1

# Make bullet less affected by gravity
BULLET_GRAVITY = 300


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Our physics engine
        self.physics_engine = None

        # Level
        self.level = 1

        # Lists
        self.wall_list = None
        self.item_list = None
        self.pig_list = None
        self.angry_bird_list = arcade.SpriteList()
        self.killed_count = 0
        self.killed_target = 0

    def setup(self, level):
        """Setup"""

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        # Player Setup
        self.player = arcade.Sprite("images/ClassicChuck2.png", SCALE)

        # Player Start X and Y
        self.player.center_x = 200
        self.player.center_y = 300

        # Player's change X and Y
        self.player.change_x = 0
        self.player.change_y = 0

        # Angry Bird Count
        self.angry_bird_count = 0

        self.all_pigs_killed = False

        self.can_bomb = True

        # Map name
        map_name = f"maps/AngryBird_level_{level}.json"

        # Load in TileMap
        tile_map = arcade.load_tilemap(map_name, SCALE)

        # Pull the sprite layers out of the tile map
        self.wall_list = tile_map.sprite_lists["Platform"]
        self.item_list = tile_map.sprite_lists["Boxes"]
        self.pig_list = tile_map.sprite_lists["Pigs"]
        self.killed_target = self.pig_list.__len__()
        print('Pig to kill', self.killed_target)

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        # clean up
        self.angry_bird_list = arcade.SpriteList()

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        # Create the items
        self.physics_engine.add_sprite_list(self.item_list, mass=1,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="item")
        for sprite in self.item_list:
            normalmass = 1
            if "mass" in sprite.properties:
                normalmass = sprite.properties["mass"]
            self.physics_engine.add_sprite(
                sprite, normalmass, DYNAMIC_ITEM_FRICTION, collision_type="item")

        # Create the pigs
        self.physics_engine.add_sprite_list(self.pig_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="item")

        # Call stuff
        self.pig_killed()

    # Sprites

    def pig_killed(self):
        """Pig Killed"""

        for sprite in self.pig_list:
            # print("angle", sprite.angle)
            if abs(sprite.angle) > 40:
                self.pig_list.remove(sprite)
                self.killed_count += 1

            elif sprite.center_x >= 1200 or sprite.center_x <= 0 or sprite.center_y >= 800 or sprite.center_y <= 0:
                self.pig_list.remove(sprite)
                self.killed_count += 1

    def angry_bird_launch(self, x, y):
        """Angry Bird Launch"""

        if self.angry_bird_count < 25:

            bird_random = random.randint(1, 3)

            # Create a bullet
            angry_bird = arcade.Sprite(
                f"images/ClassicChuck{bird_random}.png", SCALE)

            self.angry_bird_count += 1

        # Position the bullet at the player's current location
        start_x = self.player.center_x
        start_y = self.player.center_y
        angry_bird.position = self.player.position

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

        # What is the 1/2 size of this sprite, so we can figure out how far
        # away to spawn the bullet
        size = max(self.player.width, self.player.height) / 2

        # Use angle to to spawn bullet away from player in proper direction
        angry_bird.center_x += size * math.cos(angle)
        angry_bird.center_y += size * math.sin(angle)

        # Set angle of bullet
        angry_bird.angle = math.degrees(angle)

        # Gravity to use for the bullet
        # If we don't use custom gravity, bullet drops too fast, or we have
        # to make it go too fast.
        # Force is in relation to bullet's angle.
        bullet_gravity = (0, -BULLET_GRAVITY)

        # Add the sprite. This needs to be done AFTER setting the fields above.
        self.physics_engine.add_sprite(angry_bird,
                                       mass=BULLET_MASS,
                                       damping=1.0,
                                       friction=0.6,
                                       collision_type="bullet",
                                       gravity=bullet_gravity,
                                       elasticity=0.9)

        # Add force to bullet
        force = (BULLET_MOVE_FORCE, 0)
        self.physics_engine.apply_force(angry_bird, force)

        # Add the bullet to the appropriate lists
        self.angry_bird_list.append(angry_bird)

    def on_mouse_press(self, x, y, button, modifiers):
        """Mouse Press"""

        self.angry_bird_launch(x, y)

    def on_update(self, delta_time):
        """Update"""

        # Move items in the physics engine
        self.physics_engine.step()

        # Call stuff
        self.pig_killed()

        # check target count and killed count
        if self.killed_count == self.killed_target:
            self.all_pigs_killed = True

        print("Killed", self.killed_count)
        print("Target", self.killed_target)

        if self.all_pigs_killed == True:
            self.level += 1
            self.killed_count = 0
            self.setup(self.level)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.item_list.draw()
        self.wall_list.draw()
        self.pig_list.draw()
        self.angry_bird_list.draw()
        self.player.draw()

        Max_Angry_Bird = f"Shot: {self.angry_bird_count:.0f}"
        arcade.draw_text(Max_Angry_Bird, 1000, 760, arcade.color.BLACK, 20)


if __name__ == "__main__":
    window = Game()
    window.setup(window.level)
    arcade.run()
