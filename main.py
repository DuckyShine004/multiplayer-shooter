import pygame

from src.server.application.application import Application


def main():
    pygame.init()

    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Client")

    application = Application()
    application.run(window)


if __name__ == "__main__":
    main()
