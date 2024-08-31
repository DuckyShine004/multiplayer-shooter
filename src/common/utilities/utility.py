import os
import pygame

from src.common.constants.application_constants import MAX_PLAYERS
from src.common.constants.resource_constants import SPRITE_PATHS


class Utility:
    @staticmethod
    def rgb_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    @staticmethod
    def get_gun_sprite(scale=(1, 1)):
        path = os.path.join(*SPRITE_PATHS["gun"])

        return Utility.get_sprites(path, scale)[0]

    @staticmethod
    def get_player_sprites(player_id, scale=(1, 1)):
        player_index = f"player_{str(player_id % MAX_PLAYERS)}"
        path = os.path.join(*SPRITE_PATHS["players"], player_index)

        return Utility.get_sprites(path, scale)

    @staticmethod
    def get_scaled_sprite(sprite, scale):
        width, height = sprite.get_size()
        new_dimensions = (width * scale[0], height * scale[1])

        return pygame.transform.scale(sprite, new_dimensions)

    @staticmethod
    def get_sprites(path, scale):
        sprites = []

        for file_name in sorted(os.listdir(path)):
            file_path = os.path.join(path, file_name)
            sprite = pygame.image.load(file_path).convert_alpha()
            sprites.append(Utility.get_scaled_sprite(sprite, scale))

        return sprites

    @staticmethod
    def get_flipped_sprite(sprite, vertical=False, horizontal=False):
        return pygame.transform.flip(sprite, vertical, horizontal)
