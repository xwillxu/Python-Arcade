# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 150

# Classes


class Welcome(arcade.Window):
    """Main welcome window
    """

    def __init__(self):
        """Initialize the window
        """

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)
        self.time = 0
        self.color_to_choose = 0
        arcade.schedule(self.change_color, 3)

    def change_color(self, delta_time: float):
        self.color_to_choose = self.color_to_choose + 1

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        if self.color_to_choose % 3 == 0:
            arcade.draw_circle_filled(
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.BLUE
            )
        elif self.color_to_choose % 3 == 1:
            arcade.draw_circle_filled(
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.RED
            )
        else:
            arcade.draw_circle_filled(
                SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.GREEN
            )

        time_text = f"Time: {self.time:.2f}"
        arcade.draw_text(time_text, 0, 0, arcade.color.BLACK, 20)

        choose_colorToChoose_text = f"Color to choose: {self.color_to_choose}"
        arcade.draw_text(choose_colorToChoose_text, 20,
                         20, arcade.color.BLACK, 20)

    def on_update(self, delta_time):
        self.time += delta_time
