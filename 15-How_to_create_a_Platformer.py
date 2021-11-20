# How To Create A Platformer

# Import arcade
import arcade
import math
import os

# Create Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Platformer Tutorial'
BULLET_SPEED = 4
SCALE = 0.8

# Create Classes


class EnemySprite(arcade.Sprite):
    """Enemy Sprite Class"""

    def __init__(self, filename, scale):
        """Init for enemy"""
        super().__init__(filename, scale)

        self.thrust = 0
        self.max_speed = 5


class Game(arcade.Window):
    """Game Window"""

    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.EMERALD)

        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

    def enemy(self, delta_time: float):
        """Enemy Sprite"""

        enemy = arcade.Sprite(
            "arcade/arcade/resources/images/enemies/saw.png", SCALE)

        enemy.center_x = 600
        enemy.center_y = 400

        enemy.angle = 180

        self.enemy_list.append(enemy)

    def setup(self):
        """Setup"""

        # setup player
        self.player = arcade.Sprite(
            "arcade/arcade/resources/images/animated_characters/female_adventurer/femaleAdventurer_idle.png", SCALE)

        self.player.center_x = 600
        self.player.center_y = 400

        self.player.change_x = 0
        self.player.change_y = 0
        # Music
        self.background_music = arcade.load_sound(
            "RealPython/materials/arcade-a-primer/sounds/Apoxode_-_Electric_1.wav")

        self.play_music(0)
        arcade.schedule(self.play_music, 10)

        self.enemy(0)

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

        self.player.update()
        self.frame_count += 1
        #print(f'frame count', self.frame_count)
        print(f'enemy count', self.enemy_list.__len__())
        print(f'bullet count', self.bullet_list.__len__())

        for enemy in self.enemy_list:
            start_x = enemy.center_x
            start_y = enemy.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            enemy.angle = math.degrees(angle)-90

            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(
                    "arcade/arcade/resources/images/enemies/saw.png", SCALE/2)
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
        self.bullet_list.update()

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
        self.bullet_list.draw()


if __name__ == "__main__":
    window = Game()
    window.setup()
    arcade.run()
