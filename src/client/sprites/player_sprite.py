from src.common.utilities.utility import Utility


class PlayerSprite:
    def __init__(self, player_id):
        self.id = player_id
        self.sprites = Utility.get_player_sprites(player_id, (4, 4))
        self.sprite_index = 0
        self.sprite = self.sprites[0]
        self.gun_sprite = Utility.get_gun_sprite((1, 1))
        self.is_flipped = False
        self.rect = self.sprite.get_rect()
        self.gun_rect = self.gun_sprite.get_rect()

    def update(self, player):
        self.rect.x = player.position.x
        self.rect.y = player.position.y

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

        self.update_gun()

    def update_gun(self): ...

    def render(self, window):
        sprite = Utility.get_flipped_sprite(self.sprite) if self.is_flipped else self.sprite
        window.blit(sprite, self.rect)
        window.blit(self.gun_sprite, self.gun_rect)
