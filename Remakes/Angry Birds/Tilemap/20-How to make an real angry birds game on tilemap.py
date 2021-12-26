"""
Angry birds(Remake) Tilemap version + Camera version + Real
"""

"""Instrutions:

1: Click to launch a Angry Bird
2: Take down the pigs with birds
3: Random Bird Launcher
4: Can only launch 5 birds
5: Randomise the box steps
6: Have Fun
7: Made With Tilemap
8: Made With Camera
9: Make it like the real Game(Unfinished)

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

# How fast the particle will accelerate down. Make 0 if not desired
PARTICLE_GRAVITY = 0.05

# How fast to fade the particle
PARTICLE_FADE_RATE = 8

# How fast the particle moves. Range is from 2.5 <--> 5 with 2.5 and 2.5 set.
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5

# How many particles per explosion
PARTICLE_COUNT = 20

# How big the particle
PARTICLE_RADIUS = 3

# Possible particle colors
PARTICLE_COLORS = [arcade.color.ALIZARIN_CRIMSON,
                   arcade.color.COQUELICOT,
                   arcade.color.LAVA,
                   arcade.color.KU_CRIMSON,
                   arcade.color.DARK_TANGERINE]

# Chance we'll flip the texture to white and make it 'sparkle'
PARTICLE_SPARKLE_CHANCE = 0.02

# --- Smoke
# Note: Adding smoke trails makes for a lot of sprites and can slow things
# down. If you want a lot, it will be necessary to move processing to GPU
# using transform feedback. If to slow, just get rid of smoke.

# Start scale of smoke, and how fast is scales up
SMOKE_START_SCALE = 0.25
SMOKE_EXPANSION_RATE = 0.03

# Rate smoke fades, and rises
SMOKE_FADE_RATE = 7
SMOKE_RISE_RATE = 0.5

# Chance we leave smoke trail
SMOKE_CHANCE = 0.25

# Classes


class Smoke(arcade.SpriteCircle):
    """ This represents a puff of smoke """

    def __init__(self, size):
        super().__init__(size, arcade.color.LIGHT_GRAY, soft=True)
        self.change_y = SMOKE_RISE_RATE
        self.scale = SMOKE_START_SCALE

    def update(self):
        """ Update this particle """
        if self.alpha <= PARTICLE_FADE_RATE:
            # Remove faded out particles
            self.remove_from_sprite_lists()
        else:
            # Update values
            self.alpha -= SMOKE_FADE_RATE
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.scale += SMOKE_EXPANSION_RATE


class Particle(arcade.SpriteCircle):
    """ Explosion particle """

    def __init__(self, my_list):
        # Choose a random color
        color = random.choice(PARTICLE_COLORS)

        # Make the particle
        super().__init__(PARTICLE_RADIUS, color)

        # Track normal particle texture, so we can 'flip' when we sparkle.
        self.normal_texture = self.texture

        # Keep track of the list we are in, so we can add a smoke trail
        self.my_list = my_list

        # Set direction/speed
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        # Track original alpha. Used as part of 'sparkle' where we temp set the
        # alpha back to 255
        self.my_alpha = 255

        # What list do we add smoke particles to?
        self.my_list = my_list

    def update(self):
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY

            # Should we sparkle this?
            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width),
                                                          arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

            # Leave a smoke particle?
            if random.random() <= SMOKE_CHANCE:
                smoke = Smoke(5)
                smoke.position = self.position
                self.my_list.append(smoke)


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
        self.explosions_list = None

        # Killed Setup
        self.killed_count = 0
        self.killed_target = 0

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.sound.load_sound(
            ":resources:sounds/laser2.wav")
        self.hit_sound = arcade.sound.load_sound(
            ":resources:sounds/explosion2.wav")

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
        #print('Pig to kill', self.killed_target)

        # Explosion list
        self.explosions_list = arcade.SpriteList()

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

        def item_hit_handler(angry_bird, item_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            print('Got hit')

        self.physics_engine.add_collision_handler(
            "bullet", "item", post_handler=item_hit_handler)

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
        # self.physics_engine.add_sprite_list(self.item_list, mass=1,
        #                                     friction=DYNAMIC_ITEM_FRICTION,
        #                                     collision_type="item")
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
            if abs(sprite.angle) > 180:
                self.pig_list.remove(sprite)
                self.killed_count += 1

            elif sprite.center_x >= 1200 or sprite.center_x <= 0 or sprite.center_y >= 800 or sprite.center_y <= 0:
                self.pig_list.remove(sprite)
                self.killed_count += 1

    def angry_bird_launch(self, x, y):
        """Angry Bird Launch"""

        if self.angry_bird_count < 3:

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

        # Gunshot sound
        arcade.sound.play_sound(self.gun_sound)

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

        #print("Killed", self.killed_count)
        #print("Target", self.killed_target)

        if self.all_pigs_killed == True:
            self.level += 1
            self.killed_count = 0
            self.setup(self.level)

        # Loop through each bullet
        for angry_bird in self.angry_bird_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(
                angry_bird, self.item_list)

            # If it did...
            # if len(hit_list) > 0:

            # Get rid of the bullet
            # angry_bird.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for item in hit_list:
                # Make an explosion
                for i in range(PARTICLE_COUNT):
                    particle = Particle(self.explosions_list)
                    particle.position = item.position
                    self.explosions_list.append(particle)

                smoke = Smoke(50)
                smoke.position = angry_bird.position
                self.explosions_list.append(smoke)

                # coin.remove_from_sprite_lists()

                # Hit Sound
                # arcade.sound.play_sound(self.hit_sound)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.item_list.draw()
        self.wall_list.draw()
        self.pig_list.draw()
        self.angry_bird_list.draw()
        self.player.draw()
        self.explosions_list.draw()

        Max_Angry_Bird = f"Shot: {self.angry_bird_count:.0f}"
        arcade.draw_text(Max_Angry_Bird, 1000, 760, arcade.color.BLACK, 20)


if __name__ == "__main__":
    window = Game()
    window.setup(window.level)
    arcade.run()
