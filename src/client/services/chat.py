import pygame
import pygame_gui

from src.common.constants.gui_constants import CHAT_INPUT_RECT, CHAT_OUTPUT_RECT
from src.common.utilities.string_utility import StringUtility
from src.server.network.resource import Resource
from src.common.constants.application_constants import MAX_PLAYERS, TEXT_COLORS, WINDOW_RESOLUTION


class Chat:
    def __init__(self):
        self.text_entry_manager = pygame_gui.UIManager(WINDOW_RESOLUTION, "src/common/resources/gui/text/input_theme_0.json")
        self.text_box_manager = pygame_gui.UIManager(WINDOW_RESOLUTION, "src/common/resources/gui/text/output_theme_0.json")
        self.text_entry = None
        self.text_box = None
        self.message_count = 0

    def initialise(self):
        text_entry_rect = pygame.Rect(CHAT_INPUT_RECT)
        self.text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=text_entry_rect, manager=self.text_entry_manager)

        text_box_rect = pygame.Rect(CHAT_OUTPUT_RECT)
        self.text_box = pygame_gui.elements.UITextBox(html_text="", relative_rect=text_box_rect, manager=self.text_box_manager)

    def send_message(self, client):
        text = self.text_entry.get_text()

        if not text:
            return

        message = ((client.id, str(client.id) + ": "), (-2, text))
        data = {"type": "message", "message": message}
        client.send(data)
        self.text_entry.set_text("")
        self.text_entry.focus()

    def process_events(self, client, event):
        self.text_entry_manager.process_events(event)
        self.text_box_manager.process_events(event)

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            self.send_message(client)

    def update(self, client, delta_time):
        self.text_entry_manager.update(delta_time)
        self.text_box_manager.update(delta_time)
        self.update_messages(client)

    def update_messages(self, client):
        resources = client.get_resources()

        if not resources:
            return

        resource = next(iter(resources.values()))

        if not isinstance(resource, Resource):
            return

        messages = resource.get_entity("messages")
        message_count = len(messages)

        if self.message_count == 0:
            self.initialise_text_box(messages)
        elif message_count > self.message_count:
            self.update_text_box(messages, message_count)

    def initialise_text_box(self, messages):
        for (name_color, name), (text_color, text) in messages:
            name_color = self.get_text_color(name_color)
            text_color = self.get_text_color(text_color)
            self.text_box.append_html_text(f"<font color='{name_color}'>{name}<font color='{text_color}'>{text}<br>")

        self.message_count = len(messages)

    def update_text_box(self, messages, message_count):
        (name_color, name), (text_color, text) = messages[message_count - 1]
        name_color = self.get_text_color(name_color)
        text_color = self.get_text_color(text_color)
        self.text_box.append_html_text(f"<font color='{name_color}'>{name}<font color='{text_color}'>{text}<br>")

        self.message_count = message_count

    def get_text_color(self, color):
        color = TEXT_COLORS[color % MAX_PLAYERS] if color >= 0 else TEXT_COLORS[color]

        return StringUtility.rgb_to_hex(color)

    def render(self, window):
        self.text_entry_manager.draw_ui(window)
        self.text_box_manager.draw_ui(window)
