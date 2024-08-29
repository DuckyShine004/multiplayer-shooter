import pygame
import pygame_gui

from src.server.network.resource import Resource
from src.common.constants.application_constants import WINDOW_RESOLUTION


class Chat:
    def __init__(self):
        self.manager = pygame_gui.UIManager(WINDOW_RESOLUTION, "src/common/resources/gui/text/input_theme_0.json")
        self.messages = []

    def initialise(self):
        rect = pygame.Rect(100, 100, 400, 50)
        pygame_gui.elements.UITextEntryLine(relative_rect=rect, manager=self.manager)

    def send_message(self, client, element):
        message = (client.id, element.get_text())
        data = {"type": "message", "message": message}
        client.send(data)
        element.set_text("")
        element.focus()

    def process_events(self, client, event):
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            self.send_message(client, event.ui_element)

    def update(self, client, delta_time):
        self.manager.update(delta_time)
        self.update_messages(client)

    def update_messages(self, client):
        resources = client.get_resources()

        if not resources:
            return

        resource = next(iter(resources.values()))

        if not isinstance(resource, Resource):
            return

        self.messages = resource.get_entity("messages")
        print(self.messages)

    def render(self, window):
        self.manager.draw_ui(window)
