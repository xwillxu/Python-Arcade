# Platformer

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = 'Platformer'

PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 20


class Game(arcade.Window):
    """Game window for Platformer"""

    def __init__(self):
        '''Setup'''

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.player = arcade.Sprite(
            "images\player_2\player_stand.png"
        )

        self.player.center_x = 128
        self.player.center_y = 128

        self.player.change_x = 0
        self.player.change_y = 0

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        self.wall_list = arcade.SpriteList()

        map_name = ":resources:tmx_maps/map.tmx"
        my_map = arcade.tilemap.read_tmx(map_name)
        platforms_layer_name = 'Platforms'

        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=platforms_layer_name,
                                                      scaling=0.5,
                                                      use_spatial_hash=True)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             1)

    def on_key_press(self, key, modifiers):
        '''Key Press'''
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers: int):
        '''Key Release'''
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def on_update(self, delta_time: int):
        '''Update'''

        self.physics_engine.update()

    def on_draw(self):
        '''Draw'''

        arcade.start_render()

        self.player.draw()
        self.wall_list.draw()


if __name__ == "__main__":
    app = Game()
    arcade.run()
