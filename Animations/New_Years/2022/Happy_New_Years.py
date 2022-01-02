# Happy New Years

import arcade
import math
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = " Happy New Year's day"

# --- Explosion Particles Related

# How fast the particle will accelerate down. Make 0 if not desired
PARTICLE_GRAVITY = 0.05

# How fast to fade the particle
PARTICLE_FADE_RATE = 8

# How fast the particle moves. Range is from 2.5 <--> 5 with 2.5 and 2.5 set.
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5

# How many particles per explosion
PARTICLE_COUNT = 20

# How big the particle
PARTICLE_RADIUS = 3

# Possible particle colors
PARTICLE_COLORS = [arcade.color.JADE, arcade.color.TURQUOISE_BLUE,
                   arcade.color.TURQUOISE,
                   arcade.color.DARK_BLUE,
                   arcade.color.BABY_BLUE]

# arcade.color.TURQUOISE_BLUE]
# arcade.color.TURQUOISE,
# arcade.color.DARK_BLUE,
# arcade.color.BABY_BLUE,

# Another set of colors
"""arcade.color.ALIZARIN_CRIMSON,
                   arcade.color.COQUELICOT,
                   arcade.color.LAVA,
                   arcade.color.KU_CRIMSON,
                   arcade.color.DARK_TANGERINE,"""


# Chance we'll flip the texture to white and make it 'sparkle'
PARTICLE_SPARKLE_CHANCE = 0.05

# --- Smoke
# Note: Adding smoke trails makes for a lot of sprites and can slow things
# down. If you want a lot, it will be necessary to move processing to GPU
# using transform feedback. If to slow, just get rid of smoke.

# Start scale of smoke, and how fast is scales up
SMOKE_START_SCALE = 0.25
SMOKE_EXPANSION_RATE = 0.03

# Rate smoke fades, and rises
SMOKE_FADE_RATE = 7
SMOKE_RISE_RATE = 0.5

# Chance we leave smoke trail
SMOKE_CHANCE = 0.25


class Smoke(arcade.SpriteCircle):
    """ This represents a puff of smoke """

    def __init__(self, size):
        super().__init__(size, arcade.color.LIGHT_GRAY, soft=True)
        self.change_y = SMOKE_RISE_RATE
        self.scale = SMOKE_START_SCALE

    def update(self):
        """ Update this particle """
        if self.alpha <= PARTICLE_FADE_RATE:
            # Remove faded out particles
            self.remove_from_sprite_lists()
        else:
            # Update values
            self.alpha -= SMOKE_FADE_RATE
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.scale += SMOKE_EXPANSION_RATE


class Particle(arcade.SpriteCircle):
    """ Explosion particle """

    def __init__(self, my_list):
        # Choose a random color
        color = random.choice(PARTICLE_COLORS)

        # Make the particle
        super().__init__(PARTICLE_RADIUS, color)

        # Track normal particle texture, so we can 'flip' when we sparkle.
        self.normal_texture = self.texture

        # Keep track of the list we are in, so we can add a smoke trail
        self.my_list = my_list

        # Set direction/speed
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        # Track original alpha. Used as part of 'sparkle' where we temp set the
        # alpha back to 255
        self.my_alpha = 255

        # What list do we add smoke particles to?
        self.my_list = my_list

    def update(self):
        """ Update the particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Update
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY

            # Should we sparkle this?
            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width),
                                                          arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

            # Leave a smoke particle?
            if random.random() <= SMOKE_CHANCE:
                smoke = Smoke(5)
                smoke.position = self.position
                self.my_list.append(smoke)


class Animation(arcade.Window):
    """Animation"""

    def __init__(self):
        """Init"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self):
        """Setup"""

        arcade.set_background_color(arcade.color.MIDNIGHT_BLUE)

        self.frame_count = 1

        self.explosions_list = arcade.SpriteList()

    def on_draw(self):
        """Draw"""

        arcade.start_render()

        self.explosions_list.draw()

    def on_update(self, delta_time):
        """Update"""

        self.frame_count += 1

        self.explosions_list.update()

        if self.frame_count % 20 == 0:
            # Make an explosion
            for i in range(PARTICLE_COUNT):
                particle = Particle(self.explosions_list)
                particle.center_x = SCREEN_WIDTH / 2
                particle.center_y = SCREEN_HEIGHT / 2
                self.explosions_list.append(particle)

            smoke = Smoke(50)
            particle.center_x = SCREEN_WIDTH / 2
            particle.center_y = SCREEN_HEIGHT / 2
            self.explosions_list.append(smoke)

            # Make an explosion
            for i in range(PARTICLE_COUNT):
                particle = Particle(self.explosions_list)
                particle.center_x = SCREEN_WIDTH / 4
                particle.center_y = SCREEN_HEIGHT / 2
                self.explosions_list.append(particle)

            smoke = Smoke(50)
            particle.center_x = SCREEN_WIDTH / 4
            particle.center_y = SCREEN_HEIGHT / 2
            self.explosions_list.append(smoke)

            # Make an explosion
            for i in range(PARTICLE_COUNT):
                particle = Particle(self.explosions_list)
                particle.center_x = SCREEN_WIDTH / 1.5
                particle.center_y = SCREEN_HEIGHT / 2
                self.explosions_list.append(particle)

            smoke = Smoke(50)
            particle.center_x = SCREEN_WIDTH / 1.5
            particle.center_y = SCREEN_HEIGHT / 2
            self.explosions_list.append(smoke)


if __name__ == "__main__":
    window = Animation()
    window.setup()
    arcade.run()
