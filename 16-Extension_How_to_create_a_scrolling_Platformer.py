"""
Platformer Game
"""
import arcade

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
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
SPRITE_SIZE = 64


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

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
        self.engine_list = []

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

        # self.enemy_list = self.tile_map.sprite_lists["Enemies"]
        # print(self.enemy_list.__len__())
        # for sprite in self.enemy_list:
        #     sprite.change_x = -10

        self.enemy_count = 11
        self.enemy_offset = 600
        for i in range(self.enemy_count):
            slime = arcade.Sprite(
                "images/enemies/slimeBlue.png", 0.5)

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

            print("center x", slime.center_x, "boundary right",
                  slime.boundary_right, "boundary left", slime.boundary_left)

            self.enemy_list.append(slime)

            # Create the 'physics engine for enemy'
            engine = arcade.PhysicsEnginePlatformer(
                slime, self.scene.get_sprite_list(
                    "Platforms", ), GRAVITY
            )
            self.engine_list.append(engine)

        for i in range(self.enemy_count):
            bee = arcade.Sprite(
                "images/enemies/bee.png", 0.5)

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
            bee.change_x = 2
            bee.change_y = 2

            self.enemy_list.append(bee)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        self.enemy_list.draw()

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

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - \
            (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time: float):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        for engine in self.engine_list:
            engine.update()

        self.enemy_list.update()

        if self.hit:
            self.hit_timer += delta_time
            if self.hit_timer > 2.0:
                arcade.close_window()
            return

        self.enemy_list.update()

        for sprite in self.enemy_list:
            if self.player_sprite.collides_with_sprite(sprite):
                sprite.remove_from_sprite_lists()
                arcade.close_window()

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

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Coins")
        )

        danger_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Dangers"))

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        for danger in danger_hit_list:
            arcade.play_sound(self.game_over)
            self.hit = True

        # print(self.end_of_map)
        # print(self.player_sprite.center_x)
        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1
            self.setup(self.level)

        # Position the camera
        self.center_camera_to_player()


def main():
    """Main method"""
    window = MyGame()
    window.setup(window.level)
    arcade.run()


if __name__ == "__main__":
    main()
