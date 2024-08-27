import pygame

from src.server.application.application import Application


def main():
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Client")

    application = Application()
    application.run(window)


if __name__ == "__main__":
    main()
