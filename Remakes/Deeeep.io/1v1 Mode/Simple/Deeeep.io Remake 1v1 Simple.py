# Deeeep.io Remake

"""
Instrutions:
1. Point to where you want to go so that you will move
2. Kill the AI 
3. If you get killed start again
4. Only 1 skin to try out :(
5. Avoid being hit to heal
6. Defeat the AI
7. Have Fun"""

from helper import follow_sprite
import arcade
import math
import random

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
                                         color=arcade.color.RED)

        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)


# see reference in https://api.arcade.academy/en/latest/examples/sprite_move_angle.html


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.AI_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        self.set_fullscreen(not self.fullscreen)

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

        self.speed = 5
        self.score = 0
        self.ai_score = 0

        self.player_weapon = arcade.Sprite(
            "images/Tiger_Shark_head.png", SCALE)

        self.ai_weapon = arcade.Sprite("images/Tiger_Shark_head.png", SCALE)

        self.player = Health_Sprite(
            "images/Tiger_Shark.png", SCALE, max_health=900)
        self.player.center_x = 600
        self.player.center_y = 400
        self.player.change_x = 0
        self.player.change_y = 0

        self.shark_center_x = self.player.center_x
        self.shark_center_y = self.player.center_y

        self.boost_timer = 0

        self.boost_timer_start = False

        self.ai_center_x = 0
        self.ai_center_y = 0

        self.orb_list = arcade.SpriteList()
        self.orb_list2 = arcade.SpriteList()
        self.fish_list = arcade.SpriteList()

        for i in range(50):
            self.GreenOrb()
        for i in range(50):
            self.BlueOrb()
        for i in range(5):
            self.fish()

        self.AI()

        self.frame_count = 0

    def GreenOrb(self):
        """Orb"""

        center_x = random.randint(10, 1890)
        center_y = random.randint(10, 1040)
        orb = arcade.Sprite("images/Orb.png", SCALE / 4)

        orb.center_x = center_x
        orb.center_y = center_y

        self.orb_list.append(orb)

    def BlueOrb(self):
        """Orb"""

        center_x = random.randint(10, 1890)
        center_y = random.randint(10, 1040)
        orb = arcade.Sprite("images/Orb2.png", SCALE / 4)

        orb.center_x = center_x
        orb.center_y = center_y

        self.orb_list2.append(orb)

    def fish(self):
        """fish"""

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

        self.player_move(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        """Mouse Release"""

        self.boost_timer_start = True

    def AI(self):
        """AI shark"""

        AI_shark = Health_Sprite(
            "images/Tiger_Shark.png", SCALE, max_health=900)

        AI_shark.center_x = 1290
        AI_shark.center_y = 640

        AI_shark.change_x = 0
        AI_shark.change_y = 0

        self.ai_center_x = AI_shark.center_x
        self.ai_center_y = AI_shark.center_y

        self.AI_list.append(AI_shark)

    def on_key_press(self, symbol: int, modifiers: int):
        if arcade.key.SPACE:
            self.set_fullscreen(not self.fullscreen)

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.player.draw()

        self.orb_list.draw()
        self.orb_list2.draw()
        self.fish_list.draw()
        self.AI_list.draw()

        output = f"Your Score: {self.score}"
        arcade.draw_text(output, 10, 1000, arcade.color.SUNSET, 19)

        output = f"AI Score: {self.ai_score}"
        arcade.draw_text(output, 10, 900, arcade.color.SUNSET, 19)

        arcade.draw_lrtb_rectangle_filled(
            0, 200000, 100, 0, arcade.color.BRONZE_YELLOW)

        for sprite in self.AI_list:
            sprite.draw_health_bar()

        self.player.draw_health_bar()
        self.player_weapon.draw()
        self.player.draw_hit_box(arcade.color.RED, 10)

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

        if self.frame_count % 5 == 0:
            for ai in self.AI_list:
                if self.player_weapon.collides_with_sprite(ai):
                    ai.cur_health -= 90
                if self.ai_weapon.collides_with_sprite(self.player):
                    self.player.cur_health -= 90

                    print("player_hp", self.player.cur_health)

                if self.player.cur_health <= 0:
                    arcade.close_window()
                if ai.cur_health <= 0:
                    ai.remove_from_sprite_lists()

        for ai in self.AI_list:
            if not ai.cur_health >= 900:
                if self.frame_count % 10 == 0:
                    ai.cur_health += 20

        if not self.player.cur_health >= 900:
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
            self.speed = 10
        else:
            self.speed = 5

        for orb in self.orb_list:
            if self.player.collides_with_sprite(orb):
                orb.remove_from_sprite_lists()
                self.score += 1
                self.GreenOrb()

            for ai in self.AI_list:
                if ai.collides_with_sprite(orb):
                    orb.remove_from_sprite_lists()
                    self.ai_score += 1
                    self.GreenOrb()

        for orb in self.orb_list2:
            if self.player.collides_with_sprite(orb):
                orb.remove_from_sprite_lists()
                self.score += 1
                self.BlueOrb()
            for ai in self.AI_list:
                if ai.collides_with_sprite(orb):
                    orb.remove_from_sprite_lists()
                    self.ai_score += 1
                    self.BlueOrb()

        for fish in self.fish_list:

            if self.player.collides_with_sprite(fish):
                fish.remove_from_sprite_lists()
                self.score += 5
                self.fish()
            for ai in self.AI_list:
                if ai.collides_with_sprite(fish):
                    fish.remove_from_sprite_lists()
                    self.ai_score += 5
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

            if shark.cur_health > 450:
                print(shark.cur_health, 'attack current health')

                x_diff = player.center_x - shark.center_x
                y_diff = player.center_y - shark.center_y

                angle = math.atan2(y_diff, x_diff)

                shark.angle = math.degrees(angle) - 90

                shark.change_x = math.cos(angle) * 4.5
                shark.change_y = math.sin(angle) * 4.5

            else:
                print(shark.cur_health, 'run away current health')
                x_diff = player.center_x - shark.center_x
                y_diff = player.center_y - shark.center_y

                angle = math.atan2(y_diff, x_diff)

                shark.angle = - math.degrees(angle) - 90

                shark.change_x = - math.cos(angle) * 4.5
                shark.change_y = - math.sin(angle) * 4.5


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
