import pygame
from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, img, x, y, msg):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.msg = self.addText(msg)

    def addText(self, msg):
        font = pygame.font.SysFont(None, 56, bold=True)
        text = font.render(msg, 1, (255, 255, 255))
        return text

    def isClicked(self, mouse_x, mouse_y):
        if (mouse_x >= self.x and mouse_x <= self.x + 5 * PIXEL) and (
            mouse_y >= self.y and mouse_y <= self.y + 2 * PIXEL
        ):
            return True
        return False

    def draw(self, screen):
        image = pygame.transform.scale(self.image, (5 * PIXEL, 2 * PIXEL))
        screen.blit(image, (self.x, self.y))
        screen.blit(
            self.msg,
            self.msg.get_rect(center=(self.x + 2.5 * PIXEL, self.y + 1.1 * PIXEL)),
        )
