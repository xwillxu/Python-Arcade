# Deeeep.io Remake

"""
Instrutions:
1. Point to where you want to go so that you will move
2. Kill the AI 
3. Try out new skins
4. If you get killed start again
5. Don't like your skin? Click on the pause button,
then click on skins, and change into a new skin.(You
will not heal.)
6. Avoid being hit to heal
7. Choose a form of AI to play against.
8. Have Fun(As Always)"""


import arcade
import math
import random
from helper import follow_sprite, collision


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Deeeep.io 1v1 Remake"

TINY_SCALE = 0.7
SCALE = 0.4
SUPER_SCALE = 0.2


# HealthBar Setup
HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 10
HEALTHBAR_OFFSET_Y = 50

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


    # 7
    'Orca': {
        'health': 900,
        'speed': 100,
        'damage': 160,
        'scale': 0.4
    },
    # 8
    'Polar_Bear': {
        'health': 900,
        'speed': 100,
        'damage': 160,
        'scale': 0.4
    },
    # 9
    'Sleeper_Shark': {
        'health': 1000,
        'speed': 80,
        'damage': 160,
        'scale': 0.4
    },
    # 10
    'Sperm_Whale': {
        'health': 1200,
        'speed': 85,
        'damage': 160,
        'scale': 0.55
    },

    'Sunfish': {
        'health': 900,
        'speed': 100,
        'damage': 140,
        'scale': 0.4
    },

    # 11
    'Tiger_Shark': {
        'health': 800,
        'speed': 100,
        'damage': 160,
        'scale': 0.4
    },

    # 12
    'Walrus': {
        'health': 900,
        'speed': 90,
        'damage': 140,
        'scale': 0.3
    },


}


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

# see reference in https://api.arcade.academy/en/latest/examples/sprite_move_angle.html


# Game Class
class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # List Setup
        self.AI_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

    def check_win_lose(self, delta_time):
        if self.you_won != None:
            arcade.close_window()

    def setup(self):
        """Setup"""

        arcade.schedule(self.check_win_lose, 15)

        # Fullscreen Control
        self.set_fullscreen(not self.fullscreen)

        # Add Backround Color
        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        # Set Random Player Animal At The Start Of The Game
        animal_index = random.randint(1, 15)
        # print(f"Animal index is {animal_index}")
        animal_name = animal_name_list[animal_index - 1]
        # print(f"Animal name is {animal_name}")
        animal_attributes = animals[animal_name]
        # print(animal_attributes)

        self.animal_name = animal_name

        # Some Varibles Setup
        self.speed = animal_attributes['speed']
        self.score = 0
        self.ai_score = 0
        self.animal_attributes = animal_attributes
        self.you_won = None

        self.AI_animal_attributes = None

        # Players Weapon
        self.player_weapon = arcade.Sprite(
            "images/Animal1_Head.png", animal_attributes['scale'])

        # Player Setup
        self.player = Health_Sprite(
            f"images/Deeeep.io/{animal_name}.png", animal_attributes['scale'], max_health=animal_attributes["health"])
        self.player.center_x = 600
        self.player.center_y = 400
        self.player.change_x = 0
        self.player.change_y = 0
        self.player_name = animal_name
        self.player_speed = self.speed

        self.player_list.append(self.player)
        self.player_list.append(self.player_weapon)

        # Player Position Varibles
        self.shark_center_x = self.player.center_x
        self.shark_center_y = self.player.center_y

        # Boost Varibles
        self.boost_timer = 0

        self.boost_timer_start = False

        # AI's Center X And Y Varible
        self.ai_center_x = 0
        self.ai_center_y = 0

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

        # Spawn AI
        self.AI()

        # Frame Count Varible
        self.frame_count = 0

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

        if fish.center_x >= self.shark_center_x or fish.center_x <= self.shark_center_x or fish.center_y >= self.shark_center_y or fish.center_y <= self.shark_center_y:
            x_diff = self.shark_center_x + fish.center_x
            y_diff = self.shark_center_y + fish.center_y

            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            fish.angle = math.degrees(angle) - 90

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            fish.change_x = math.cos(angle) * 4.5
            fish.change_y = math.sin(angle) * 4.5

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called whenever the mouse button is clicked. """

        # Player Movement Function
        self.player_move(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """Mouse Release"""

        # Start Boost
        self.boost_timer_start = True

    def AI(self):
        """AI shark"""

        animal_index = random.randint(1, 15)

        animal_name = animal_name_list[animal_index - 1]

        animal_attributes = animals[animal_name]

        self.AI_animal_attributes = animal_attributes

        # AI's Weapon
        self.ai_weapon = arcade.Sprite(
            "images/Animal1_Head.png", self.AI_animal_attributes['scale'])

        # AI Setup
        AI_shark = Health_Sprite(
            f"images/Deeeep.io/{animal_name}.png", animal_attributes['scale'], max_health=animal_attributes['health'])

        AI_shark.center_x = 1290
        AI_shark.center_y = 640

        AI_shark.change_x = 0
        AI_shark.change_y = 0

        # Place AI's center x and y in varibles
        self.ai_center_x = AI_shark.center_x
        self.ai_center_y = AI_shark.center_y

        # Add to AI list
        self.AI_list.append(AI_shark)

    def Win(self):
        """You Won"""

        self.you_won = True

    def Lose(self):
        """You Lost"""

        self.you_won = False

    def on_key_press(self, symbol: int, modifiers: int):
        " Key Press"
        # Fullscreen Control
        if arcade.key.SPACE:
            self.set_fullscreen(not self.fullscreen)

    def on_draw(self):
        """Draw"""

        # Start Rendering
        arcade.start_render()

        # Draw Player

        # Draw The Player List
        self.player_list.draw()
        # Try To Draw The Health Bars If Not Skip To Next Object in Player List
        for player in self.player_list:
            try:
                player.draw_health_bar()
            except:
                pass
            finally:
                pass

        # Draw Lists
        self.orb_list.draw()
        self.orb_list2.draw()
        self.fish_list.draw()
        self.AI_list.draw()

        # Draw Your Score
        output = f"Your Score: {self.score}"
        arcade.draw_text(output, 10, 1000, arcade.color.SUNSET, 19)

        # Draw AI Score
        output = f"AI Score: {self.ai_score}"
        arcade.draw_text(output, 10, 900, arcade.color.SUNSET, 19)

        # Draw Ground
        arcade.draw_lrtb_rectangle_filled(
            0, 200000, 100, 0, arcade.color.BRONZE_YELLOW)

        # Draw Health Bars
        for sprite in self.AI_list:
            sprite.draw_health_bar()

        # self.player_weapon.draw_hit_box()
        # self.ai_weapon.draw_hit_box()

        if self.you_won == True:
            arcade.draw_text(" YOU WON! ", 500, 500,
                             arcade.color.GREEN, 100)

        elif self.you_won == False:
            arcade.draw_text(" YOU LOST☹ ", 500, 500,
                             arcade.color.RED, 100)

    def player_move(self, x, y):
        """Player Move"""

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

    def on_update(self, delta_time):
        """Update"""

        self.player.update()
        self.fish_list.update()
        self.AI_list.update()

        self.frame_count += 1

        self.shark_center_x = self.player.center_x
        self.shark_center_y = self.player.center_y

        if self.player_name == "Tiger_Shark":
            if self.player.center_y <= 300:
                self.speed == 7
            else:
                self.speed == 6
        if self.player_name == "Elephant_Seal":
            if self.player.cur_health < 800:
                self.animal_attributes["damage"] += 9
            else:
                self.animal_attributes["damage"] == 120
            if self.player.cur_health < 700:
                self.speed == 5.5
            else:
                self.speed == 5
            if self.player.cur_health < 700:
                self.animal_attributes["damage"] += 18
            else:
                self.animal_attributes["damage"] == 120

            if self.player.cur_health < 600:
                self.animal_attributes["damage"] += 27
            else:
                self.animal_attributes["damage"] == 120
            if self.player.cur_health < 500:
                self.speed == 6
            else:
                self.speed == 5
            if self.player.cur_health < 500:
                self.animal_attributes["damage"] += 36
            else:
                self.animal_attributes["damage"] == 120
            if self.player.cur_health < 400:
                self.animal_attributes["damage"] += 45
            else:
                self.animal_attributes["damage"] == 120
            if self.player.cur_health < 300:
                self.animal_attributes["damage"] += 54
            else:
                self.animal_attributes["damage"] == 120
            if self.player.cur_health < 200:
                self.animal_attributes["damage"] += 63
            else:
                self.animal_attributes["damage"] == 120
            if self.player.cur_health < 100:
                self.animal_attributes["damage"] += 72
            else:
                self.animal_attributes["damage"] == 120

        if self.frame_count % 5 == 0:
            for ai in self.AI_list:
                # If game is over, don't do any more collision
                if self.you_won != None:
                    continue
                if self.player_weapon.collides_with_sprite(ai):
                    ai.cur_health -= self.animal_attributes['damage']
                    if self.animal_name == "Marlin":
                        if not self.frame_count % 300 == 0:
                            if self.frame_count % 5 == 0:
                                ai.cur_health -= 20
                if self.ai_weapon.collides_with_sprite(self.player):
                    self.player.cur_health -= self.animal_attributes['damage']

                    print("player_hp", self.player.cur_health)

                    if self.animal_name == "Marlin":
                        if not self.frame_count % 300 == 0:
                            if self.frame_count % 10 == 0:
                                self.player.cur_health -= 20

                if self.player.cur_health <= 0:
                    self.player.remove_from_sprite_lists()
                    self.player_weapon.remove_from_sprite_lists()
                    self.Lose()
                    print("Lose")

                if ai.cur_health <= 0:
                    ai.remove_from_sprite_lists()
                    self.Win()
                    print("Win")

        for ai in self.AI_list:
            if not ai.cur_health >= ai.max_health:
                if self.frame_count % 10 == 0:
                    ai.cur_health += 20

        if not self.player.cur_health >= self.player.max_health:
            if self.frame_count % 10 == 0:
                self.player.cur_health += 20

        if self.boost_timer_start == True:
            self.boost_timer += 0.06

        if self.boost_timer >= 10:
            self.boost_timer_start = False
            self.boost_timer = 0

        for fish in self.fish_list:
            distancex = abs(fish.center_x - self.shark_center_x)
            distancey = abs(fish.center_y - self.shark_center_y)
            distance = math.sqrt(distancex * distancex + distancey * distancey)
            # print(distance, 'distance')
            if distance < 300:
                # print('too close, run away')
                x_diff = self.shark_center_x - fish.center_x
                y_diff = self.shark_center_y - fish.center_y

                angle = math.atan2(y_diff, x_diff)

                # Angle the bullet sprite so it doesn't look like it is flying
                # sideways.
                fish.angle = math.degrees(angle) + 90

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                fish.change_x = - math.cos(angle) * 4.5
                fish.change_y = - math.sin(angle) * 4.5

        if self.boost_timer > 0:
            self.speed = self.animal_attributes['speed'] / 9 / 2 * 2
        else:
            self.speed = self.animal_attributes['speed'] / 9 / 2

        for orb in self.orb_list:
            if self.player.collides_with_sprite(orb):
                orb.remove_from_sprite_lists()
                self.score += 1
                if self.player.cur_health <= self.player.max_health:
                    self.player.cur_health += 10
                self.GreenOrb()

            for ai in self.AI_list:
                if ai.collides_with_sprite(orb):
                    orb.remove_from_sprite_lists()
                    self.ai_score += 1
                    if ai.cur_health <= ai.max_health:
                        ai.cur_health += 10
                    self.GreenOrb()

        for orb in self.orb_list2:
            if self.player.collides_with_sprite(orb):
                orb.remove_from_sprite_lists()
                self.score += 1
                if self.player.cur_health <= self.player.max_health:
                    self.player.cur_health += 10
                self.BlueOrb()
            for ai in self.AI_list:
                if ai.collides_with_sprite(orb):
                    orb.remove_from_sprite_lists()
                    self.ai_score += 1
                    if ai.cur_health <= ai.max_health:
                        ai.cur_health += 10
                    self.BlueOrb()

        for fish in self.fish_list:

            if self.player.collides_with_sprite(fish):
                fish.remove_from_sprite_lists()
                self.score += 5
                if self.player.cur_health <= self.player.max_health:
                    self.player.cur_health += 20
                self.fish()
            for ai in self.AI_list:
                if ai.collides_with_sprite(fish):
                    fish.remove_from_sprite_lists()
                    self.ai_score += 5
                    if ai.cur_health <= ai.max_health:
                        ai.cur_health += 20
                    self.fish()

        for ai in self.AI_list:
            if self.player.collides_with_sprite(ai):

                dest_x = self.player.center_x
                dest_y = self.player.center_y

                x_diff = dest_x - ai.center_x
                y_diff = dest_y - ai.center_y

                angle = math.atan2(y_diff, x_diff)

                ai.change_x = - self.player.change_x
                ai.change_y = - self.player.change_y
            if self.player.collides_with_sprite(ai):
                self.player.change_x = -self.player.change_x
                self.player.change_y = -self.player.change_y

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

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
        for shark in self.AI_list:
            if self.frame_count % 30 == 0:
                self.AI_move(player=self.player, shark=shark,
                             delta_time=delta_time)

        for shark in self.AI_list:
            if shark.top > self.height:
                shark.top = self.height
            if shark.right > self.width:
                shark.right = self.width
            if shark.bottom < 0:
                shark.bottom = 0
            if shark.left < 0:
                shark.left = 0

        follow_sprite(self.player_weapon, self.player, offset=0)
        for ai in self.AI_list:
            follow_sprite(self.ai_weapon, ai, offset=0)

        if self.you_won == None:
            collision(self.player_weapon, self.AI_list)

    def AI_move(self, player, shark, delta_time):
        """AI Move Command"""

        # Random Movement
        distance_to_player_x = abs(player.center_x - shark.center_x)
        distance_to_player_y = abs(player.center_y - shark.center_y)

        x_diff = None
        y_diff = None

        distance = math.sqrt(distance_to_player_x * distance_to_player_x +
                             distance_to_player_y * distance_to_player_y)
        range_of_attack = 700

        if distance > range_of_attack:
            "Go in a random direction"
            shark.change_x += random.randint(-1, 1)
            shark.change_y += random.randint(-1, 1)

            center_x_in_future = shark.center_x + shark.change_x
            center_y_in_future = shark.center_y + shark.change_y
            x_diff = center_x_in_future - shark.center_x
            y_diff = center_y_in_future - shark.center_y

            angle = math.atan2(y_diff, x_diff)

            shark.angle = math.degrees(angle) - 90

        else:

            "Attack player"

            if shark.cur_health > shark.max_health / 2:
                print(shark.cur_health, 'attack current health')

                x_diff = player.center_x - shark.center_x
                y_diff = player.center_y - shark.center_y

                angle = math.atan2(y_diff, x_diff)

                shark.angle = math.degrees(angle) - 90

                shark.change_x = math.cos(
                    angle) * self.AI_animal_attributes['speed'] / 9 / 2
                shark.change_y = math.sin(
                    angle) * self.AI_animal_attributes['speed'] / 9 / 2

            else:
                print(shark.cur_health, 'run away current health')
                x_diff = player.center_x - shark.center_x
                y_diff = player.center_y - shark.center_y

                angle = math.atan2(y_diff, x_diff) - 180

                shark.angle = - math.degrees(angle)

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
