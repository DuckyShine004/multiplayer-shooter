from src.client.sprites.gun_sprite import GunSprite
from src.common.utilities.utility import Utility


class PlayerSprite:
    def __init__(self, player_id):
        self.id = player_id
        self.sprites = Utility.get_player_sprites(player_id, (4, 4))
        self.sprite_index = 0
        self.sprite = self.sprites[0]
        self.gun_sprite = GunSprite()
        self.is_flipped = False
        self.rect = self.sprite.get_rect()

    def update(self, player):
        self.rect.center = (player.position.x, player.position.y)
        self.gun_sprite.update(player.gun)

        if player.velocity.x == player.velocity.y == 0.0:
            self.sprite_index = 0
            self.sprite = self.sprites[0]
            return

        self.sprite_index += 0.2

        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0

        self.sprite = self.sprites[int(self.sprite_index)]

        if player.velocity.x > 0:
            self.is_flipped = False
        elif player.velocity.x < 0:
            self.is_flipped = True

    def render(self, window):
        sprite = Utility.get_flipped_sprite(self.sprite, vertical=True) if self.is_flipped else self.sprite
        window.blit(sprite, self.rect)
        self.gun_sprite.render(window)
