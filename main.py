import pygame

from src.common.constants.application_constants import WINDOW_RESOLUTION
from src.server.application.application import Application


def main():
    pygame.init()

    window = pygame.display.set_mode(WINDOW_RESOLUTION)
    pygame.display.set_caption("Client")

    application = Application()

    application.initialise()
    application.run(window)


if __name__ == "__main__":
    main()
