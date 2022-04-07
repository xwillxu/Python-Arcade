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

        # Create End Of Map Varible
        self.end_of_map = 0

        # Create The Lists:
        # Enemy
        self.enemy_list = arcade.SpriteList()

        # Mining
        self.mine_list = arcade.SpriteList()

        # Engine
        self.engine_list = []

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = f"maps/Minecraft_Map_1.json"

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

        # Where Is The End Of The Map
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Hit Setup
        self.hit_timer = 0.0
        self.hit = False

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)

        # Center X
        self.player_sprite.center_x = 72
        # Center Y
        self.player_sprite.center_y = 500
        # Add To Scene
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

    def Start_Page(self):
        """Shows When Starting The Game"""

    def mobs(self):
        """Mobs"""

    def mine(self, x, y):
        """Mining Command"""

    def jump(self):
        """Jump Command"""

        if self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

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

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # Up
        if key == arcade.key.UP or key == arcade.key.W:
            self.jump()
        # Left
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        # Right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # Left
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        # Right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        self.mine(x, y)

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


def main():
    """Main method"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
