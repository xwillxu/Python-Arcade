# How To Create A Platformer

# Import arcade
import arcade
import math
import os

# Create Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Platformer Tutorial'

# Other Varibles
BULLET_SPEED = 7
PLAYER_BULLET_SPEED = 7
ENEMY_SPEED = 3
SPRITE_SCALING_LASER = 0.8
SCALE = 0.8

# Health bar stuff
HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 6
HEALTHBAR_OFFSET_Y = -50

# Create Classes


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


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.IMPERIAL_BLUE)

        self.enemy_list = arcade.SpriteList()
        self.enemy2_list = arcade.SpriteList()
        self.enemy3_list = arcade.SpriteList()
        self.enemy4_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.player_bullet2_list = arcade.SpriteList()
        self.player_bullet3_list = arcade.SpriteList()
        self.player_bullet4_list = arcade.SpriteList()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

    def enemy(self, delta_time: float):
        """Enemy Sprite"""

        if self.enemy_count <= 0:
            enemy = Health_Sprite(
                "arcade/arcade/resources/images/enemies/saw.png", 0.5, max_health=30)

            enemy.center_x = 200
            enemy.center_y = 100
            enemy.change_x = 0
            enemy.change_y = 0

            enemy.angle = 180

            self.enemy_count += 1

            self.enemy_list.append(enemy)

            enemy_2 = Health_Sprite(
                "arcade/arcade/resources/images/enemies/saw.png", 0.5, max_health=30)

            enemy_2.center_x = 1000
            enemy_2.center_y = 700
            enemy_2.change_x = 0
            enemy_2.change_y = 0

            enemy_2.angle = 180

            self.enemy_count += 1

            self.enemy2_list.append(enemy_2)

            enemy_3 = Health_Sprite(
                "arcade/arcade/resources/images/enemies/saw.png", 0.5, max_health=30)

            enemy_3.center_x = 200
            enemy_3.center_y = 700
            enemy_3.change_x = 0
            enemy_3.change_y = 0

            enemy_3.angle = 180

            self.enemy_count += 1

            self.enemy3_list.append(enemy_3)

            enemy_4 = Health_Sprite(
                "arcade/arcade/resources/images/enemies/saw.png", 0.5, max_health=30)

            enemy_4.center_x = 1000
            enemy_4.center_y = 100
            enemy_4.change_x = 0
            enemy_4.change_y = 0

            enemy_4.angle = 180

            self.enemy_count += 1

            self.enemy4_list.append(enemy_4)

    def player_bullet(self):
        """Player Bullet"""

        if self.enemy_list.__len__() > 0:
            player_bullet = arcade.Sprite(
                ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)
            player_bullet.center_x = self.player.center_x
            player_bullet.center_y = self.player.center_y
            x_diff = self.enemy_list[0].center_x - player_bullet.center_x
            y_diff = self.enemy_list[0].center_y - player_bullet.center_y
            angle = math.atan2(y_diff, x_diff)
            x_speed = math.cos(angle) * PLAYER_BULLET_SPEED
            y_speed = math.sin(angle) * PLAYER_BULLET_SPEED
            player_bullet.angle = math.degrees(angle)

            player_bullet.velocity = (x_speed, y_speed)

            self.player_bullet_list.append(player_bullet)

        if self.enemy2_list.__len__() > 0:
            player_bullet2 = arcade.Sprite(
                ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            player_bullet2.center_x = self.player.center_x
            player_bullet2.center_y = self.player.center_y
            x_diff = self.enemy2_list[0].center_x - player_bullet2.center_x
            y_diff = self.enemy2_list[0].center_y - player_bullet2.center_y
            angle = math.atan2(y_diff, x_diff)
            x_speed = math.cos(angle) * PLAYER_BULLET_SPEED
            y_speed = math.sin(angle) * PLAYER_BULLET_SPEED
            player_bullet2.angle = math.degrees(angle)

            player_bullet2.velocity = (x_speed, y_speed)

            self.player_bullet2_list.append(player_bullet2)

        if self.enemy3_list.__len__() > 0:
            player_bullet3 = arcade.Sprite(
                ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            player_bullet3.center_x = self.player.center_x
            player_bullet3.center_y = self.player.center_y
            x_diff = self.enemy3_list[0].center_x - player_bullet3.center_x
            y_diff = self.enemy3_list[0].center_y - player_bullet3.center_y
            angle = math.atan2(y_diff, x_diff)
            x_speed = math.cos(angle) * PLAYER_BULLET_SPEED
            y_speed = math.sin(angle) * PLAYER_BULLET_SPEED
            player_bullet3.angle = math.degrees(angle)

            player_bullet3.velocity = (x_speed, y_speed)

            self.player_bullet3_list.append(player_bullet3)

        if self.enemy4_list.__len__() > 0:
            player_bullet4 = arcade.Sprite(
                ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            player_bullet4.center_x = self.player.center_x
            player_bullet4.center_y = self.player.center_y
            x_diff = self.enemy4_list[0].center_x - player_bullet4.center_x
            y_diff = self.enemy4_list[0].center_y - player_bullet4.center_y
            angle = math.atan2(y_diff, x_diff)
            x_speed = math.cos(angle) * PLAYER_BULLET_SPEED
            y_speed = math.sin(angle) * PLAYER_BULLET_SPEED
            player_bullet4.angle = math.degrees(angle)

            player_bullet4.velocity = (x_speed, y_speed)

            self.player_bullet4_list.append(player_bullet4)

    def setup(self):
        """Setup"""

        # setup player
        self.player = Health_Sprite(
            "arcade/arcade/resources/images/animated_characters/female_adventurer/femaleAdventurer_idle.png", SCALE, max_health=50)

        self.player.center_x = 800
        self.player.center_y = 400

        self.player.change_x = 0
        self.player.change_y = 0

        self.enemy_count = 0
        self.score = 0
        # Music
        self.background_music = arcade.load_sound(
            "RealPython/materials/arcade-a-primer/sounds/Apoxode_-_Electric_1.wav")

        self.play_music(0)
        arcade.schedule(self.play_music, 15.5)

        self.enemy(0)
        arcade.schedule(self.enemy, 0.1)

    def play_music(self, delta_time: float):
        arcade.play_sound(self.background_music)

    def on_key_press(self, key, modifiers):
        """On Key Press"""

        if key == arcade.key.UP:
            self.player.change_y = 7
        if key == arcade.key.DOWN:
            self.player.change_y = -7
        if key == arcade.key.RIGHT:
            self.player.change_x = 7
        if key == arcade.key.LEFT:
            self.player.change_x = -7
        if key == arcade.key.SPACE:
            self.player_bullet()

    def on_key_release(self, key, modifiers):
        """On Key Release"""
        if key == arcade.key.UP:
            self.player.change_y = 0
        if key == arcade.key.DOWN:
            self.player.change_y = 0
        if key == arcade.key.RIGHT:
            self.player.change_x = 0
        if key == arcade.key.LEFT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """On Update"""

        self.frame_count += 1
        # print(f'frame count', self.frame_count)
        # print(f'enemy count', self.enemy_list.__len__())
        # print(f'bullet count', self.bullet_list.__len__())

        for player_bullet in self.player_bullet_list:
            hit_list = arcade.check_for_collision_with_list(
                player_bullet, self.enemy_list)

            if len(hit_list) > 0:
                player_bullet.remove_from_sprite_lists()

            for enemy in hit_list:
                if not isinstance(enemy, Health_Sprite):
                    raise TypeError("List contents must all be ints")

                enemy.cur_health -= 2

                if enemy.cur_health <= 0:
                    enemy.remove_from_sprite_lists()

                    self.score += 100
                    self.enemy_count -= 1

        for player_bullet2 in self.player_bullet2_list:
            hit_list = arcade.check_for_collision_with_list(
                player_bullet2, self.enemy2_list)

            if len(hit_list) > 0:
                player_bullet2.remove_from_sprite_lists()

            for enemy_2 in hit_list:
                if not isinstance(enemy_2, Health_Sprite):
                    raise TypeError("List contents must all be ints")

                enemy_2.cur_health -= 2

                if enemy_2.cur_health <= 0:
                    enemy_2.remove_from_sprite_lists()

                    self.score += 100
                    self.enemy_count -= 1

        for player_bullet3 in self.player_bullet3_list:
            hit_list = arcade.check_for_collision_with_list(
                player_bullet3, self.enemy3_list)

            if len(hit_list) > 0:
                player_bullet3.remove_from_sprite_lists()

            for enemy_3 in hit_list:
                if not isinstance(enemy_3, Health_Sprite):
                    raise TypeError("List contents must all be ints")

                enemy_3.cur_health -= 2

                if enemy_3.cur_health <= 0:
                    enemy_3.remove_from_sprite_lists()

                    self.score += 100
                    self.enemy_count -= 1

        for player_bullet4 in self.player_bullet4_list:
            hit_list = arcade.check_for_collision_with_list(
                player_bullet4, self.enemy4_list)

            if len(hit_list) > 0:
                player_bullet4.remove_from_sprite_lists()

            for enemy_4 in hit_list:
                if not isinstance(enemy_4, Health_Sprite):
                    raise TypeError("List contents must all be ints")

                enemy_4.cur_health -= 2

                if enemy_4.cur_health <= 0:
                    enemy_4.remove_from_sprite_lists()

                    self.score += 100
                    self.enemy_count -= 1

        for enemy in self.enemy_list:
            start_x = enemy.center_x
            start_y = enemy.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            enemy.angle = math.degrees(angle)-90

            enemy.change_x = math.cos(angle) * ENEMY_SPEED
            enemy.change_y = math.sin(angle) * ENEMY_SPEED

            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(
                    "arcade/arcade/resources/images/enemies/saw.png", 0.1)
                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.angle = math.degrees(angle)

                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        for enemy_2 in self.enemy2_list:
            start_x = enemy_2.center_x
            start_y = enemy_2.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            enemy_2.angle = math.degrees(angle)-90

            enemy_2.change_x = math.cos(angle) * ENEMY_SPEED
            enemy_2.change_y = math.sin(angle) * ENEMY_SPEED

            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(
                    "arcade/arcade/resources/images/enemies/saw.png", 0.1)
                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.angle = math.degrees(angle)

                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        for enemy_3 in self.enemy3_list:
            start_x = enemy_3.center_x
            start_y = enemy_3.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            enemy_3.angle = math.degrees(angle)-90

            enemy_3.change_x = math.cos(angle) * ENEMY_SPEED
            enemy_3.change_y = math.sin(angle) * ENEMY_SPEED

            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(
                    "arcade/arcade/resources/images/enemies/saw.png", 0.1)
                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.angle = math.degrees(angle)

                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        for enemy_4 in self.enemy4_list:
            start_x = enemy_4.center_x
            start_y = enemy_4.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            enemy_4.angle = math.degrees(angle)-90

            enemy_4.change_x = math.cos(angle) * ENEMY_SPEED
            enemy_4.change_y = math.sin(angle) * ENEMY_SPEED

            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(
                    "arcade/arcade/resources/images/enemies/saw.png", 0.1)
                bullet.center_x = start_x
                bullet.center_y = start_y

                bullet.angle = math.degrees(angle)

                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        for bullet in self.bullet_list:
            if bullet.top < 0 or bullet.top > SCREEN_HEIGHT or bullet.right > SCREEN_WIDTH or bullet.right < 0:
                bullet.remove_from_sprite_lists()

        self.enemy_list.update()
        self.enemy2_list.update()
        self.enemy3_list.update()
        self.enemy4_list.update()

        self.bullet_list.update()
        self.player_bullet_list.update()
        self.player_bullet2_list.update()
        self.player_bullet3_list.update()
        self.player_bullet4_list.update()
        self.player.update()

        for bullet in self.bullet_list:
            if self.player.collides_with_sprite(bullet):
                bullet.remove_from_sprite_lists()
                self.player.cur_health -= 2
                if self.player.cur_health <= 0:
                    arcade.close_window()

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        """On Draw"""
        arcade.start_render()
        # Draw Sprites
        self.player.draw()
        self.enemy_list.draw()
        self.enemy2_list.draw()
        self.enemy3_list.draw()
        self.enemy4_list.draw()
        self.player_bullet_list.draw()
        self.player_bullet2_list.draw()
        self.player_bullet3_list.draw()
        self.player_bullet4_list.draw()
        self.bullet_list.draw()

        for enemy in self.enemy_list:
            enemy.draw_health_bar()
        for enemy_2 in self.enemy2_list:
            enemy_2.draw_health_bar()
        for enemy_3 in self.enemy3_list:
            enemy_3.draw_health_bar()
        for enemy_4 in self.enemy4_list:
            enemy_4.draw_health_bar()
        self.player.draw_health_bar()

        text = f"Score: {self.score:.0f}"
        arcade.draw_text(text, 10, 0, arcade.color.WHITE, 20)


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
