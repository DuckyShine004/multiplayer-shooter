import pygame
import pygame_gui

from src.common.utilities.utility import Utility
from src.common.constants.gui_constants import CHAT_INPUT_RECT, CHAT_OUTPUT_RECT
from src.server.network.resource import Resource
from src.common.constants.application_constants import MAX_PLAYERS, TEXT_COLORS, WINDOW_RESOLUTION


class Chat:
    def __init__(self):
        self.text_entry_manager = pygame_gui.UIManager(WINDOW_RESOLUTION, "src/common/resources/gui/text/input_theme_0.json")
        self.text_box_manager = pygame_gui.UIManager(WINDOW_RESOLUTION, "src/common/resources/gui/text/output_theme_0.json")
        self.text_entry = None
        self.text_box = None
        self.message_count = 0
        self.is_hidden = False

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

    def toggle_chat(self):
        self.is_hidden ^= True

        if self.is_hidden:
            self.text_entry.hide()
            self.text_box.hide()
        else:
            self.text_entry.show()
            self.text_box.show()

    def process_events(self, client, event):
        self.text_entry_manager.process_events(event)
        self.text_box_manager.process_events(event)

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            self.send_message(client)

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            text = self.text_entry.get_text()
            self.text_entry.set_text(text[:-1] if text and text[-1] == "\\" else text)
            self.text_entry.focus()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSLASH:
            self.toggle_chat()

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
        for message in messages:
            html_message = self.get_html_message(message)
            self.text_box.append_html_text(html_message)

        self.message_count = len(messages)

    def update_text_box(self, messages, message_count):
        html_message = self.get_html_message(messages[message_count - 1])
        self.text_box.append_html_text(html_message)
        self.message_count = message_count

    def get_html(self, message):
        color, text = self.get_text_color(message[0]), message[1]
        font = "Determination Mono Web"
        size = "4.5"

        return f"<font face='{font}' color='{color}' size='{size}'>{text}</font>"

    def get_html_message(self, message):
        name, text = message

        name_html = self.get_html(name)
        text_html = self.get_html(text)

        return f"{name_html}{text_html}<br>"

    def get_text_color(self, color):
        color = TEXT_COLORS[color % MAX_PLAYERS] if color >= 0 else TEXT_COLORS[color]

        return Utility.rgb_to_hex(color)

    def render(self, window):
        self.text_entry_manager.draw_ui(window)
        self.text_box_manager.draw_ui(window)
