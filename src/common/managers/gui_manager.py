import pygame_gui

from src.client.sprites.connection_sprite import ConnectionSprite
from src.client.services.chat import Chat
from src.common.constants.application_constants import WINDOW_RESOLUTION


class GUIManager:
    def __init__(self):
        self.manager = pygame_gui.UIManager(WINDOW_RESOLUTION, "src/common/resources/gui/text/input_theme_0.json")
        self.chat = Chat()
        self.connection_sprite = ConnectionSprite()
        self.native_elements = []
        self.custom_elements = []
        self.fonts = []

    def initialise(self):
        self.chat.initialise()

    def is_chat_hidden(self):
        return self.chat.is_hidden

    def process_events(self, client, event):
        self.manager.process_events(event)
        self.chat.process_events(client, event)

    def update(self, client, delta_time):
        self.manager.update(delta_time)
        self.chat.update(client, delta_time)
        self.connection_sprite.update(client)

    def render(self, window):
        self.manager.draw_ui(window)
        self.chat.render(window)
        self.connection_sprite.render(window)
