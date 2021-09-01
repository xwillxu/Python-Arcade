# Basic arcade drawing
# Draw smiley face

import arcade
import random
import math
import os

SCREEN_WIDTH = 1950
SCREEN_HEIGHT = 950
SCREEN_TITLE = "Basic Drawing"
RADIUS = 150

HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 6
HEALTHBAR_OFFSET_Y = -10


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
                                         height=5,
                                         color=arcade.color.RED)

        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - 10,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)


class Game(arcade.Window):
    '''Main drawing window 
       and moving face. Shooter game,
       with a smiley face being controled by you.
       Angry faces will appear on the left side,
       they will head to the right at different
       speeds. Plus there is a boundary so you
       can't get off the screen. self. tank. music.
    '''

    def __init__(self):
        '''Initalize the drawing window
        '''
        # Backround
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.health = 100
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprites
        # Spawn the player
        self.player = arcade.Sprite(
            "images\Smiling_Face_Emoji.png", 0.07
        )

        self.player.center_x = 0

        self.player.center_y = 0

        self.player.change_x = 0
        self.player.change_y = 0

        self.tank_count = 0
        self.tank_health = 0
        self.jet_count = 0
        self.collided = False
        self.collision_timer = 0.0
        self.bullet_score = 0

        # Sprite lists
        self.fighter_jet_lists = arcade.SpriteList()
        self.jet_missle_lists = arcade.SpriteList()
        self.jet_missle_lists_2 = arcade.SpriteList()
        self.jet_missle_lists_3 = arcade.SpriteList()
        self.tank_lists = arcade.SpriteList()
        self.tank_missle_lists = arcade.SpriteList()

        self.enemy_lists = arcade.SpriteList()

        self.bullet_lists = arcade.SpriteList()
        # Spawn the player

        self.player.center_x = 40
        self.player.center_y = 300

        self.player.shoot = False

        # schedule always happen in setup/init
        arcade.schedule(self.spawn_enemy, 1.0)

        # schedule always happen in setup/init
        arcade.schedule(self.spawn_tank, 1.0)

        arcade.schedule(self.spawn_tank_missle, 4)

        arcade.schedule(self.fighter_jet, 1.0)

        arcade.schedule(self.jet_missle, 2)

        arcade.schedule(self.play_music, 16)

        # Music
        self.music = arcade.load_sound(
            "RealPython/materials/arcade-a-primer/sounds/Apoxode_-_Electric_1.wav")

        self.collision_sound = arcade.load_sound(
            "RealPython/materials/arcade-a-primer/sounds/Collision.wav")

        self.game_over = arcade.load_sound("sounds/gameover1.wav")

        self.play_music(0)

    def play_music(self, delta_time: float):
        arcade.play_sound(
            self.music)

    def spawn_bullet(self):
        # Spawn a bullet based on play position
        # what is the scaling? The image may be big.
        bullet = arcade.Sprite(
            "RealPython/materials/arcade-a-primer/images/missile.png", 1.5, 0, 0, 0, 0, 0, 0, 1, 1, True)

        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y

        bullet.velocity = (200, 0)

        # add to the list so that we can update them/draw them as in the list conveniently
        self.bullet_lists.append(bullet)

    def spawn_enemy(self, delta_time: float):
        """Adds a new enemy to the screen
            using schedule.
        """

        # what is the scaling? The image may be big.
        enemy = arcade.Sprite("images/angry_face.png", 0.04)

        enemy.left = random.randint(1950, 1950)
        enemy.top = random.randint(0, 1000)

        enemy.velocity = (random.randint(-200, -50), 0)

        # add to the list so that we can update them/draw them as in the list conveniently
        self.enemy_lists.append(enemy)

    def spawn_tank(self, delta_time: float):
        """ Spawns tank that 
            shoots at you.
        """
        if self.tank_count < 3:
            tank = Health_Sprite(
                "images/tank.png", 0.05,
                max_health=30)
            tank.left = 1950
            tank.top = random.randint(50, 900)

            tank.velocity = (-150, 0)
            self.tank_health = 20
            self.tank_lists.append(tank)
            self.tank_count += 1

    def spawn_tank_missle(self, delta_time: float):
        """missles that come out from the tanks
        """

        for tank in self.tank_lists:

            tank_missle = arcade.Sprite(
                "RealPython/materials/arcade-a-primer/images/missile.png")
            total_speed = 200
            tank_missle.center_x = tank.center_x
            tank_missle.center_y = tank.center_y
            x_diff = self.player.center_x - tank_missle.center_x
            y_diff = self.player.center_y - tank_missle.center_y
            angle = math.atan2(y_diff, x_diff)

            tank_missle.angle = math.degrees(angle) + 180

            x_speed = math.cos(angle) * total_speed
            y_speed = math.sin(angle) * total_speed

            tank_missle.velocity = (x_speed, y_speed)

            self.tank_missle_lists.append(tank_missle)

    def fighter_jet(self, delta_time: float):
        """Fighter_jet_boss"""
        if self.jet_count <= 0:
            jet = Health_Sprite(
                "images/fighter_jet.png", 0.5, max_health=100
            )

            jet.left = 1200
            jet.top = 475

            jet.velocity = (-200, 0)

            self.fighter_jet_lists.append(jet)
            self.jet_count += 1

    def jet_missle(self, delta_time: float):
        """ jets missles"""

        for jet in self.fighter_jet_lists:

            jet_missle = arcade.Sprite(
                "images/blue_laser.png", 0.05)
            total_speed = 200
            jet_missle.center_x = jet.center_x
            jet_missle.center_y = jet.center_y
            x_diff = self.player.center_x - jet_missle.center_x
            y_diff = self.player.center_y - jet_missle.center_y
            angle = math.atan2(y_diff, x_diff)

            jet_missle.angle = math.degrees(angle) + 180

            x_speed = math.cos(angle) * total_speed
            y_speed = math.sin(angle) * total_speed

            jet_missle.velocity = (x_speed, y_speed)

            self.jet_missle_lists.append(jet_missle)

            jet_missle_2 = arcade.Sprite(
                "images/blue_laser.png", 0.05)
            total_speed = 200
            jet_missle_2.center_x = jet.center_x
            jet_missle_2.center_y = jet.center_y
            x_diff = self.player.center_x - jet_missle_2.center_x + 80
            y_diff = self.player.center_y - jet_missle_2.center_y + 80
            angle = math.atan2(y_diff, x_diff)

            jet_missle_2.angle = math.degrees(angle) + 180

            x_speed = math.cos(angle) * total_speed
            y_speed = math.sin(angle) * total_speed

            jet_missle_2.velocity = (x_speed, y_speed)

            self.jet_missle_lists_2.append(jet_missle_2)

            jet_missle_3 = arcade.Sprite(
                "images/blue_laser.png", 0.05)
            total_speed = 200
            jet_missle_3.center_x = jet.center_x
            jet_missle_3.center_y = jet.center_y
            x_diff = self.player.center_x - jet_missle_3.center_x - 80
            y_diff = self.player.center_y - jet_missle_3.center_y - 80
            angle = math.atan2(y_diff, x_diff)

            jet_missle_3.angle = math.degrees(angle) + 180

            x_speed = math.cos(angle) * total_speed
            y_speed = math.sin(angle) * total_speed

            jet_missle_3.velocity = (x_speed, y_speed)

            self.jet_missle_lists_3.append(jet_missle_3)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT:
            # Quit immediately
            self.player.change_x = 5
        if symbol == arcade.key.LEFT:
            # Quit immediately
            self.player.change_x = -5
        if symbol == arcade.key.UP:
            # Quit immediately
            self.player.change_y = 5
        if symbol == arcade.key.DOWN:
            # Quit immediately
            self.player.change_y = -5
        if symbol == arcade.key.SPACE:
            self.spawn_bullet()

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT:
            # Quit immediately
            self.player.change_x = 0
        if symbol == arcade.key.LEFT:
            # Quit immediately
            self.player.change_x = 0
        if symbol == arcade.key.UP:
            # Quit immediately
            self.player.change_y = 0
        if symbol == arcade.key.DOWN:
            # Quit immediately
            self.player.change_y = 0

    def on_update(self, delta_time: float):

        super().on_update(delta_time)
        self.player.center_x = self.player.center_x + self.player.change_x

        super().on_update(delta_time)
        self.player.center_y = self.player.center_y + self.player.change_y

        if self.health == 0 or self.health < 0:
            self.collision_timer += delta_time
            if self.collision_timer > 1.0:
                arcade.close_window()
            return

        for enemy in self.enemy_lists:
            if self.player.collides_with_sprite(enemy):
                self.collided = False
                enemy.remove_from_sprite_lists()
                self.health -= 5
                arcade.play_sound(self.collision_sound)
                if self.health == 0 or self.health < 0:
                    arcade.play_sound(
                        self.game_over)

        for tank_missle in self.tank_missle_lists:
            if self.player.collides_with_sprite(tank_missle):
                self.collided = False
                tank_missle.remove_from_sprite_lists()
                self.health -= 2
                arcade.play_sound(self.collision_sound)
                if self.health == 0 or self.health < 0:
                    arcade.play_sound(
                        self.game_over)

        for jet_missle in self.jet_missle_lists:
            if self.player.collides_with_sprite(jet_missle):
                self.collided = False
                jet_missle.remove_from_sprite_lists()
                self.health -= 5
                arcade.play_sound(self.collision_sound)
                if self.health == 0 or self.health < 0:
                    self.collision_timer += delta_time
                    arcade.play_sound(
                        self.game_over)

        for jet_missle_2 in self.jet_missle_lists_2:
            if self.player.collides_with_sprite(jet_missle_2):
                self.collided = False
                jet_missle_2.remove_from_sprite_lists()
                self.health -= 5
                arcade.play_sound(self.collision_sound)
                if self.health == 0 or self.health < 0:
                    arcade.play_sound(
                        self.game_over)

        for jet_missle_3 in self.jet_missle_lists_3:
            if self.player.collides_with_sprite(jet_missle_3):
                self.collided = False
                jet_missle_3.remove_from_sprite_lists()
                self.health -= 5
                arcade.play_sound(self.collision_sound)
                if self.health == 0 or self.health < 0:
                    arcade.play_sound(
                        self.game_over)

        for enemy in self.enemy_lists:
            if enemy.collides_with_list(self.bullet_lists):
                enemy.remove_from_sprite_lists()
                self.bullet_score += 5

        for bullet in self.bullet_lists:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.tank_lists)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for tank in hit_list:
                if not isinstance(tank, Health_Sprite):
                    raise TypeError("List contents must all be ints")

                tank.cur_health -= 2

                if tank.cur_health <= 0:
                    tank.remove_from_sprite_lists()

                    self.bullet_score += 100
                    self.tank_count -= 1

        for bullet in self.bullet_lists:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.fighter_jet_lists)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for jet in hit_list:
                if not isinstance(jet, Health_Sprite):
                    raise TypeError("List contents must all be ints")

                jet.cur_health -= 2

                if jet.cur_health <= 0:
                    jet.remove_from_sprite_lists()

                    self.bullet_score += 500
                    self. jet_count -= 1

        # IMPORTANT, without this, the sprites will NOT move at all
        # Update the position of enemies based on speed
        for sprite in self.enemy_lists:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
        for sprite in self.bullet_lists:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )

        for sprite in self.tank_lists:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            if sprite.center_x < 1500:
                sprite.center_x = 1500
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )

        for sprite in self.tank_missle_lists:
            sprite.center_x = sprite.center_x + sprite.change_x * delta_time
            sprite.center_y = sprite.center_y + sprite.change_y * delta_time

        for sprite in self.fighter_jet_lists:
            sprite.center_x = sprite.center_x + sprite.change_x * delta_time
            if sprite.center_x < 1100:
                sprite.center_x = 1100
            sprite.center_y = sprite.center_y + sprite.change_y * delta_time

        for sprite in self.jet_missle_lists:
            sprite.center_x = sprite.center_x + sprite.change_x * delta_time
            sprite.center_y = sprite.center_y + sprite.change_y * delta_time

        for sprite in self.jet_missle_lists_2:
            sprite.center_x = sprite.center_x + sprite.change_x * delta_time
            sprite.center_y = sprite.center_y + sprite.change_y * delta_time

        for sprite in self.jet_missle_lists_3:
            sprite.center_x = sprite.center_x + sprite.change_x * delta_time
            sprite.center_y = sprite.center_y + sprite.change_y * delta_time

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

        for tank in self.tank_lists:
            start_x = tank.center_x
            start_y = tank.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            tank.angle = math.degrees(angle) + 180

        for jet in self.fighter_jet_lists:
            start_x = jet.center_x
            start_y = jet.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            jet.angle = math.degrees(angle) + -90

    def on_draw(self):
        '''Called when needed to draw
        '''

        arcade.start_render()

        # IMPORTANT
        # Without this, nothing will show!!!
        self.enemy_lists.draw()
        self.player.draw()
        self.bullet_lists.draw()
        self.tank_lists.draw()
        self.tank_missle_lists.draw()
        self.fighter_jet_lists.draw()
        self.jet_missle_lists.draw()
        self.jet_missle_lists_2.draw()
        self.jet_missle_lists_3.draw()

        for tank in self.tank_lists:
            tank.draw_health_bar()

        for jet in self.fighter_jet_lists:
            jet.draw_health_bar()

        time_text = f"Score: {self.bullet_score:.0f}"
        arcade.draw_text(time_text, 10, 0, arcade.color.BLACK, 20)

        time_text = f"Health: {self.health:.0f}"
        arcade.draw_text(time_text, 1700, 0, arcade.color.LIGHT_GREEN, 20)


if __name__ == "__main__":
    app = Game()
    arcade.run()


# Instructions :
# To move use the arrow keys
# Dodge bullets and angry faces
# Space to shoot at enemys
