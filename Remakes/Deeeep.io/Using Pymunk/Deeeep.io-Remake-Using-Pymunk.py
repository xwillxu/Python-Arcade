"""

This Is My Deeeep.io Version Using Pymunk 
So That The Collision And Stuff Like That Is Not Crappy.

"""

# Import Librarys And Modules
import arcade
import random
import math
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

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

# Movement Forces For Different Sprites In The Physic Engine
PLAYER_MOVE_FORCE = 4000
AI_MOVE_FORCE = 4000

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
        'scale': 0.6
    },

    # 3
    "Elephant_Seal": {
        'health': 1000,
        'speed': 90,
        'damage': 120,
        'scale': 0.45
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
        'scale': 0.5
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
        'scale': 0.53
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
        'scale': 0.32
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
        self.AI_list = None

        # Physic Engine
        self.physics_engine: Optional[PymunkPhysicsEngine] = None

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        # Set Random Player Animal At The Start Of The Game
        animal_index = random.randint(1, 15)
        animal_name = animal_name_list[animal_index - 1]
        animal_attributes = animals[animal_name]

        # Use Animal Attributes For Self Not Just For Setup
        self.animal_name = animal_name
        self.animal_attributes = animal_attributes

        # AI Animal Attributes
        self.AI_animal_attributes = None

        # Boost Varibles
        self.boost_timer = 0
        self.boost_timer_start = False

        # Frame Count
        self.frame_count = 0

        # Player
        self.player = Health_Sprite(
            f"images/Deeeep.io/{animal_name}.png", animal_attributes["scale"], max_health=animal_attributes["health"])
        self.player.center_x = random.randint(10, 1190)
        self.player.center_y = random.randint(10, 790)

        # Speed
        self.speed = animal_attributes['speed'] / 9 / 2

        # Food Setup / Activate Lists
        self.orb_list = arcade.SpriteList()
        self.orb_list2 = arcade.SpriteList()
        self.fish_list = arcade.SpriteList()
        self.AI_list = arcade.SpriteList()

        # Spawn Food
        for i in range(50):
            self.GreenOrb()
        for i in range(50):
            self.BlueOrb()
        for i in range(5):
            self.fish()

        # Spawn AI
        self.AI()

        # Score
        self.score = 0

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = 0.7

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, 0)

        # Create the physics engine
        self.physics_engine = PymunkPhysicsEngine(damping=damping,
                                                  gravity=gravity)

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player, mass=10,
                                       friction=0.01,
                                       damping=0.5,
                                       elasticity=0.8,
                                       collision_type="player",
                                       max_velocity=400)

        # Create some boxes to push around.
        # Mass controls, well, the mass of an object. Defaults to 1.
        self.physics_engine.add_sprite_list(self.AI_list,
                                            mass=10,
                                            friction=0.01,
                                            elasticity=0.8,
                                            damping=1,
                                            collision_type="rock")

    def AI(self):
        """AI Shark"""
        # Index, Name, And Attributes
        animal_index = random.randint(10, 10)
        animal_name = animal_name_list[animal_index - 1]
        animal_attributes = animals[animal_name]

        # Set AI Attributes
        self.AI_animal_attributes = animal_attributes

        AI_Shark = Health_Sprite(
            f"images/Deeeep.io/{animal_name}.png", animal_attributes["scale"], animal_attributes["health"])

        AI_Shark.center_x = random.randint(10, 1190)
        AI_Shark.center_y = random.randint(10, 790)

        AI_Shark.change_x = 0
        AI_Shark.change_y = 0

        # Place AI's center x and y in varibles
        self.ai_center_x = AI_Shark.center_x
        self.ai_center_y = AI_Shark.center_y

        # Add to AI list
        self.AI_list.append(AI_Shark)

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
        print('set angle', self.player.angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        # self.player.change_x = math.cos(angle) * self.speed
        # self.player.change_y = math.sin(angle) * self.speed
        self.physics_engine.set_velocity(self.player,
                                         (math.cos(angle) * self.speed * 100, math.sin(angle) * self.speed * 100))
        #forceX = math.cos(angle) * PLAYER_MOVE_FORCE
        #forceY = math.sin(angle) * PLAYER_MOVE_FORCE
        #force = (forceX, forceY)
        #print('apply force', force)
        #self.physics_engine.apply_force(self.player, force)

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

    def on_mouse_press(self, x, y, button, modifiers):
        """Mouse Press"""

        self.boost_timer_start = True

    def on_mouse_motion(self, x, y, dx, dy):
        """Mouse Motion"""

        self.player_movement(x, y)

    def on_key_press(self, key, modifiers):
        """Key Press"""

        # Controls
        if arcade.key.SPACE:
            self.set_fullscreen(not self.fullscreen)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        # Draw The Player
        self.player.draw()

        # Draw Lists
        self.orb_list.draw()
        self.orb_list2.draw()
        self.fish_list.draw()
        self.AI_list.draw()

        # Draw Your Score
        output = f"Your Score: {self.score}"
        arcade.draw_text(output, 10, 1000, arcade.color.SUNSET, 19)

    def on_update(self, delta_time):
        """Update"""

        # Update Everything
        self.player.update()
        self.orb_list.update()
        self.orb_list2.update()
        self.fish_list.update()
        self.AI_list.update()

        # --- Move items in the physics engine
        self.physics_engine.step()

        # Change Frame Count By 1
        self.frame_count += 1

        # Make The Fish Run Away From Player In Certian Distance
        for fish in self.fish_list:
            # Distance X and Y
            distancex = abs(fish.center_x - self.player.center_x)
            distancey = abs(fish.center_y - self.player.center_y)
            distance = math.sqrt(distancex * distancex + distancey * distancey)
            if distance < 300:
                # X diff And Y diff
                x_diff = self.player.center_x - fish.center_x
                y_diff = self.player.center_y - fish.center_y

                # Angle
                angle = math.atan2(y_diff, x_diff)

                # Angle the sprite so it doesn't look like it is flying sideways.
                fish.angle = math.degrees(angle) + 90

                # Taking into account the angle, calculate our change_x and change_y. Velocity is how fast the sprite travels.
                fish.change_x = - math.cos(angle) * 4.5
                fish.change_y = - math.sin(angle) * 4.5

        for fish in self.fish_list:
            if fish.top > self.height:
                fish.remove_from_sprite_lists()
                self.fish()
            if fish.right > self.width:
                fish.remove_from_sprite_lists()
                self.fish()
            if fish.bottom < 0:
                fish.remove_from_sprite_lists()
                self.fish()
            if fish.left < 0:
                fish.remove_from_sprite_lists()
                self.fish()

        # Boost Code
        if self.boost_timer_start == True:
            self.boost_timer += 0.3

        # Timer
        if self.boost_timer >= 5.5:
            self.boost_timer_start = False
            self.boost_timer = 0

        #  Actual Boosting
        if self.boost_timer > 0:
            self.speed = self.animal_attributes['speed'] / 9 / 2 * 3
        else:
            self.speed = self.animal_attributes['speed'] / 9 / 2

        # Keep The Player From Going Off The Screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

        # Call AI Movement
        for shark in self.AI_list:
            if self.frame_count % 30 == 0:
                self.AI_move(player=self.player, shark=shark,
                             delta_time=delta_time)

        # Green Orb Collision
        for orb in self.orb_list:
            if self.player.collides_with_sprite(orb):
                orb.remove_from_sprite_lists()
                self.score += 1
                self.GreenOrb()

        # Blue Orb Collision
        for orb in self.orb_list2:
            if self.player.collides_with_sprite(orb):
                orb.remove_from_sprite_lists()
                self.score += 1
                self.BlueOrb()

        # Fish Collision
        for fish in self.fish_list:
            if self.player.collides_with_sprite(fish):
                fish.remove_from_sprite_lists()
                self.score += 5
                self.fish()

    def AI_move(self, player, shark, delta_time):
        """AI Move Command"""

        # Random Movement
        distance_to_player_x = abs(player.center_x - shark.center_x)
        distance_to_player_y = abs(player.center_y - shark.center_y)

        # X and Y Diff
        x_diff = None
        y_diff = None

        # Distance
        distance = math.sqrt(distance_to_player_x * distance_to_player_x +
                             distance_to_player_y * distance_to_player_y)

        # The Range Where The AI See's The Player
        range_of_attack = 700

        # Real Movement Code
        if distance > range_of_attack:
            "Go in a random direction"

            # Chnage x and Change y
            shark.change_x += random.randint(-1, 1)
            shark.change_y += random.randint(-1, 1)

            # Center X And Y In The Future
            center_x_in_future = shark.center_x + shark.change_x
            center_y_in_future = shark.center_y + shark.change_y

            # X And Y Diff Activated
            x_diff = center_x_in_future - shark.center_x
            y_diff = center_y_in_future - shark.center_y

            # Angle
            angle = math.atan2(y_diff, x_diff)

            # Change Angle
            shark.angle = math.degrees(angle) - 90

        else:
            "Attack player"

            # Another If And Else
            # If AI's Health Is Larger Than 1/2 Of It's Max Health Attack
            if shark.cur_health > shark.max_health / 2:

                # X And Y Diff Activated
                x_diff = player.center_x - shark.center_x
                y_diff = player.center_y - shark.center_y

                # Angle
                angle = math.atan2(y_diff, x_diff)

                # Change Angle
                shark.angle = math.degrees(angle) - 90

                # Shark Speed X And Y
                change_x = math.cos(
                    angle) * self.AI_animal_attributes['speed'] / 9 / 2
                change_y = math.sin(
                    angle) * self.AI_animal_attributes['speed'] / 9 / 2

                self.physics_engine.set_velocity(shark,
                                                 (change_x * 50, change_y * 50))

            else:
                # Run Away
                # X And Y Diff Activated
                x_diff = player.center_x - shark.center_x
                y_diff = player.center_y - shark.center_y

                # Angle
                angle = math.atan2(y_diff, x_diff) - 180

                # Change Angle
                shark.angle = - math.degrees(angle)

                # Shark Speed X And Y
                shark.change_x = - \
                    math.cos(angle) * \
                    self.AI_animal_attributes['speed'] / 9 / 2
                shark.change_y = - \
                    math.sin(angle) * \
                    self.AI_animal_attributes['speed'] / 9 / 2


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
