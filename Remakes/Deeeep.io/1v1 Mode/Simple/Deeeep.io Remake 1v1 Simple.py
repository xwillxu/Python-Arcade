# Deeeep.io Remake

"""
Instrutions:
1. Point to where you want to go so that you will move
2. Kill the AI 
3. If you get killed start again
4. Only 3 skins to try out :(
5. Avoid being hit to heal
6. Defeat the AI
7. Have Fun"""

import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Deeeep.io 1v1 Remake"


class Game(arcade.Window):
    """Game"""

    def __init__(self):
        """Init"""

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
