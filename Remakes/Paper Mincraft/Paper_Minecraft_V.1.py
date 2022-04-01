"""
Platformer Game
"""
import arcade
import math
import os

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer Extention"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 20
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
SPRITE_SIZE = 64

BULLET_SPEED = 30
BOSS_BULLET_SPEED = 10

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


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics enginea
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        self.level = 3

        self.end_of_map = 0

        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.engine_list = []
        self.shield_list = arcade.SpriteList()

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(
            ":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        self.game_over = arcade.load_sound("sounds/gameover1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self, level):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = f"maps/Xwill's_json_map{level}.json"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, TILE_SCALING, layer_options)

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.hit_timer = 0.0
        self.hit = False

        # Enemy Setup

        self.enemy_count = 11
        self.enemy_offset = 600

        self.frame_count = 1

        # Shield setup
        self.damage = 0
        self.shield_count = 0

        # Create the Player Sprite lists
        player_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 72
        self.player_sprite.center_y = 500
        self.scene.add_sprite("Player", self.player_sprite)

        # --- Other stuff
        # Set the background color
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(
                self.tile_map.tiled_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.scene.get_sprite_list(
                "Platforms", ), GRAVITY
        )

        # self.manualEnemy()

        enemyFromTilemap = self.tile_map.sprite_lists["Enemy_With_Gravity"]
        self.tiledEnemyWithGravity(enemyFromTilemap)
        for original in self.tile_map.sprite_lists["Enemy_With_Gravity"]:
            original.center_x = -100

        BossFromTilemap = self.tile_map.sprite_lists["Boss"]
        self.Boss(BossFromTilemap)
        for original in self.tile_map.sprite_lists["Boss"]:
            original.center_x = -100

        enemyNoGravityFromTilemap = self.tile_map.sprite_lists["Enemy"]
        self.tiledEnemyBee(enemyNoGravityFromTilemap)
        for original in self.tile_map.sprite_lists["Enemy"]:
            original.center_x = -100

    def tiledEnemyBee(self, enemyNoGravityFromTilemap):
        for enemy in enemyNoGravityFromTilemap:
            initial_x = enemy.center_x
            initial_y = enemy.center_y
            enemy = Health_Sprite(
                "images/enemies/bee.png", 0.5, 10)

            enemy.center_x = initial_x
            enemy.center_y = initial_y

            fly_range_x = 400
            fly_range_y = 75

            # Set boundaries on the left/right the enemy can't cross
            enemy.boundary_right = initial_x + fly_range_x
            enemy.boundary_left = initial_x - fly_range_x

            enemy.boundary_top = initial_y + fly_range_y
            enemy.boundary_bottom = initial_y - fly_range_y
            enemy.change_x = 5
            enemy.change_y = 3

            # print("center x", slime.center_x, "boundary right",
            # slime.boundary_right, "boundary left", slime.boundary_left)

            self.enemy_list.append(enemy)

    def Boss(self, BossFromTilemap):
        for Boss in BossFromTilemap:
            initial_x = Boss.center_x
            initial_y = Boss.center_y
            Boss = Health_Sprite(
                "images/enemies/SlimeMonster.png", 0.25, 100)
            crawl_range = 1000
            Boss.center_x = initial_x
            Boss.center_y = initial_y

            # Set boundaries on the left/right the enemy can't cross
            Boss.boundary_right = initial_x + crawl_range
            Boss.boundary_left = initial_x - crawl_range
            Boss.change_x = 10

            Boss.properties["Boss"] = True

            # print("center x", slime.center_x, "boundary right",
            # slime.boundarwwy_right, "boundary left", slime.boundary_left)

            self.enemy_list.append(Boss)

            # Create the 'physics engine for enemy'
            engine = arcade.PhysicsEnginePlatformer(
                Boss, self.scene.get_sprite_list(
                    "Platforms", ), GRAVITY
            )
            self.engine_list.append(engine)

    def tiledEnemyWithGravity(self, enemyFromTilemap):
        for enemy in enemyFromTilemap:
            initial_x = enemy.center_x
            initial_y = enemy.center_y
            enemy = Health_Sprite(
                "images/enemies/slimeBlock.png", 0.5, 10)
            crawl_range = 400
            enemy.center_x = initial_x
            enemy.center_y = initial_y

            # Set boundaries on the left/right the enemy can't cross
            enemy.boundary_right = initial_x + crawl_range
            enemy.boundary_left = initial_x - crawl_range
            enemy.change_x = 5

            # print("center x", slime.center_x, "boundary right",
            # slime.boundary_right, "boundary left", slime.boundary_left)

            self.enemy_list.append(enemy)

            # Create the 'physics engine for enemy'
            engine = arcade.PhysicsEnginePlatformer(
                enemy, self.scene.get_sprite_list(
                    "Platforms", ), GRAVITY
            )
            self.engine_list.append(engine)

    def mobs(self):
        """Mobs"""
        for i in range(self.enemy_count):
            slime = Health_Sprite(
                "images/enemies/slimeBlue.png", 0.5, 10)

            slime.bottom = SPRITE_SIZE * 4
            slime.left = SPRITE_SIZE * 4

            initial_x = self.enemy_offset + i * 1000
            crawl_range = 400
            slime.center_x = initial_x
            slime.center_y = 1200

            print(slime.center_x)

            # Set boundaries on the left/right the enemy can't cross
            slime.boundary_right = initial_x + crawl_range
            slime.boundary_left = initial_x - crawl_range
            slime.change_x = 5

            # print("center x", slime.center_x, "boundary right",
            # slime.boundary_right, "boundary left", slime.boundary_left)

            self.enemy_list.append(slime)

            # Create the 'physics engine for enemy'
            engine = arcade.PhysicsEnginePlatformer(
                slime, self.scene.get_sprite_list(
                    "Platforms", ), GRAVITY
            )
            self.engine_list.append(engine)

        for i in range(self.enemy_count):
            bee = Health_Sprite(
                "images/enemies/bee.png", 0.5, 10)

            bee.bottom = SPRITE_SIZE * 4
            bee.left = SPRITE_SIZE * 4

            initial_x = self.enemy_offset + i * 1000
            initial_y = 620
            fly_range_x = 400
            fly_range_y = 50
            bee.center_x = initial_x
            bee.center_y = initial_y

            # Set boundaries on the left/right the enemy can't cross
            bee.boundary_right = initial_x + fly_range_x
            bee.boundary_left = initial_x - fly_range_x
            bee.boundary_bottom = initial_y - fly_range_y
            bee.boundary_top = initial_y + fly_range_y
            bee.change_x = 3
            bee.change_y = 3

            self.enemy_list.append(bee)

    def mine(self, x, y):
        """Mining Command"""

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Actddddivate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        for sprite in self.enemy_list:
            sprite.draw_health_bar()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.shield_list.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        self.bullet(x, y)

    def center_camera_to_player(self):
        """Center The Camera To The Player"""
        # Center The Screen X
        screen_center_x = self.player_sprite.center_x - (
            self.camera.viewport_width / 2
        )

        # Center The Screen Y
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        # Make Sure The Screen Dose Not Lose The Player
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        # Make Sure That The Screen And Player Are In Sync
        player_centered = screen_center_x, screen_center_y

        # Send The Camera To The Player
        self.camera.move_to(player_centered)

    def on_update(self, delta_time: float):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update Everything Else
        self.bullet_list.update()
        self.enemy_list.update()

        # Update Engine
        for engine in self.engine_list:
            engine.update()

        # Add Frames To Frame Count
        self.frame_count += 1

        # If Lost All Hp Die
        if self.hit:
            self.hit_timer += delta_time
            if self.hit_timer > 2.0:
                arcade.close_window()
            return

        self.enemy_list.update()

        # Check each enemy
        for enemy in self.enemy_list:
            # checking x boundary
            # If the enemy hit the left boundary, reverse
            if enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                enemy.change_x *= -1
            # If the enemy hit the right boundary, reverse
            elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                enemy.change_x *= -1
            # checking y boundary
            if enemy.boundary_top is not None and enemy.top > enemy.boundary_top:
                enemy.change_y *= -1
            # If the enemy hit the right boundary, reverse
            elif enemy.boundary_bottom is not None and enemy.bottom < enemy.boundary_bottom:
                enemy.change_y *= -1

        # See If You Touch Anything Dangerous
        danger_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Dangers"))

        # Make Sure That You Add All The Dangers
        for danger in danger_hit_list:
            arcade.play_sound(self.game_over)
            self.hit = True

        # Position the camera
        self.center_camera_to_player()

        # Make Sure The Bullet Dose Not Go Off The Screen
        for bullet in self.bullet_list:
            if bullet.center_x < 0:
                bullet.remove_from_sprite_lists()

            if bullet.center_x - self.camera.position.x > 1200:
                bullet.remove_from_sprite_lists()
            if bullet.center_y < 0:
                bullet.remove_from_sprite_lists()
            if bullet.center_y - self.camera.position.y > 800:
                bullet.remove_from_sprite_lists()


def main():
    """Main method"""
    window = MyGame()
    window.setup(window.level)
    arcade.run()


if __name__ == "__main__":
    main()
