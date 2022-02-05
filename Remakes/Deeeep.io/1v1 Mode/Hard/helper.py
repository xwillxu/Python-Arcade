import math


def find_offset(sprite, offset=50):
    rad = math.radians(sprite.angle)
    center_x = sprite.center_x - math.sin(rad) * offset
    center_y = sprite.center_y + math.cos(rad) * offset
    return center_x, center_y


def follow_sprite(sprite, your_target_sprite, offset=50):
    center_x, center_y = find_offset(your_target_sprite, offset)
    sprite.center_x = center_x
    sprite.center_y = center_y
    sprite.angle = your_target_sprite.angle


def collision(player, ai_list):
    for ai in ai_list:
        if player.collides_with_sprite(ai):

            ai.change_x = - player.change_x * 2
            ai.change_y = - player.change_y * 2

        if player.collides_with_sprite(ai):

            player.change_x = - player.change_x * 2
            player.change_y = - player.change_y * 2
