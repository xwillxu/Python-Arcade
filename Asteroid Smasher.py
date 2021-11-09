"""Asteroid Smasher"""

import arcade
import math
import os
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Asteroid Smasher"
OFFSCREEN_SPACE = 300
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE


class TurningSprite(arcade.Sprite):
    """ Sprite that sets its angle to the direction it is traveling in. """

    def update(self):
        """ Move the sprite """
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))


class PlayerShip(arcade.Sprite):
    """Player Ship"""

    def __init__(self, filename, scale):
        super().__init__(filename, scale)

        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05

        self.center_x = 500
        self.center_y = 350

    def update(self):
        """ Update for Player"""

        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0

        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y

        super().update()


class AsteroidSprite(arcade.Sprite):
    """ Sprite that represents an asteroid. """

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0

    def update(self):
        """ Move the asteroid around. """
        super().update()
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.objects = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.player_ship_list = arcade.SpriteList()

    def setup(self):
        """Setup"""

        self.player_ship = PlayerShip(
            "arcade/arcade/resources/images/space_shooter/playerShip2_orange.png", 0.5)

        self.score = 0

        self.objects.append(self.player_ship)
        arcade.set_background_color(arcade.color.BLACK)

        image_list = (":resources:images/space_shooter/meteorGrey_big1.png",
                      ":resources:images/space_shooter/meteorGrey_big2.png",
                      ":resources:images/space_shooter/meteorGrey_big3.png",
                      ":resources:images/space_shooter/meteorGrey_big4.png")
        for i in range(3):
            image_no = random.randrange(4)
            enemy_sprite = AsteroidSprite(image_list[image_no], 0.5)
            enemy_sprite.guid = "Asteroid"

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1

            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.asteroid_list.append(enemy_sprite)

    def on_key_press(self, key, modifiers):
        """Key press"""

        if key == arcade.key.UP:
            self.player_ship.thrust = 5
        elif key == arcade.key.W:
            self.player_ship.thrust = 5
        elif key == arcade.key.D:
            self.player_ship.change_angle = -3
        elif key == arcade.key.RIGHT:
            self.player_ship.change_angle = -3
        elif key == arcade.key.S:
            self.player_ship.thrust = -5
        elif key == arcade.key.DOWN:
            self.player_ship.thrust = -5
        elif key == arcade.key.A:
            self.player_ship.change_angle = 3
        elif key == arcade.key.LEFT:
            self.player_ship.change_angle = 3
        elif key == arcade.key.SPACE:
            self.bullet()

    def on_key_release(self, key, modifiers):
        """Key release"""
        if key == arcade.key.UP:
            self.player_ship.thrust = 0
        elif key == arcade.key.W:
            self.player_ship.thrust = 0
        elif key == arcade.key.S:
            self.player_ship.thrust = 0
        elif key == arcade.key.DOWN:
            self.player_ship.thrust = 0
        elif key == arcade.key.A:
            self.player_ship.change_angle = 0
        elif key == arcade.key.LEFT:
            self.player_ship.change_angle = 0
        elif key == arcade.key.D:
            self.player_ship.change_angle = 0
        elif key == arcade.key.RIGHT:
            self.player_ship.change_angle = 0

    def on_update(self, delta_time):
        """Update"""

        self.asteroid_list.update()

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.asteroid_list)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for enemy_sprite in hit_list:

                self.split_asteroid()

                if enemy_sprite.size <= 0:
                    self.score += 16

        for sprite in self.objects:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
            sprite.update()

        if self.player_ship.top > self.height:
            self.player_ship.top = self.height
        if self.player_ship.right > self.width:
            self.player_ship.right = self.width
        if self.player_ship.bottom < 0:
            self.player_ship.bottom = 0
        if self.player_ship.left < 0:
            self.player_ship.left = 0

    def bullet(self):
        """Ship's Bullet"""

        bullet = TurningSprite(
            ":resources:images/space_shooter/laserBlue01.png", 0.6)
        bullet.guid = "Bullet"

        bullet_speed = 13
        bullet.change_y = \
            math.cos(math.radians(self.player_ship.angle)) * bullet_speed
        bullet.change_x = \
            -math.sin(math.radians(self.player_ship.angle)) \
            * bullet_speed

        bullet.center_x = self.player_ship.center_x
        bullet.center_y = self.player_ship.center_y
        bullet.update()

        self.bullet_list.append(bullet)
        self.objects.append(bullet)

    def split_asteroid(self, asteroid: AsteroidSprite):
        """ Split an asteroid into chunks. """
        x = asteroid.center_x
        y = asteroid.center_y
        self.score += 1

        if asteroid.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                              ":resources:images/space_shooter/meteorGrey_med2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              0.5 * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                self.asteroid_list.append(enemy_sprite)
                self.objects.append(enemy_sprite)

        elif asteroid.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_small1.png",
                              ":resources:images/space_shooter/meteorGrey_small2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              0.5 * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                self.asteroid_list.append(enemy_sprite)
                self.objects.append(enemy_sprite)

        elif asteroid.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_tiny1.png",
                              ":resources:images/space_shooter/meteorGrey_tiny2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              0.5 * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.asteroid_list.append(enemy_sprite)
                self.objects.append(enemy_sprite)

    def on_draw(self):

        arcade.start_render()

        self.objects.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
