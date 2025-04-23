import pygame
from settings import *
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Battleship(pygame.sprite.Sprite):
    def __init__(self, length, x, y, orientation: Orientation) -> None:
        super().__init__()
        self.sprite = pygame.Surface((3 * PIXEL, PIXEL))
        self.x = x * PIXEL
        self.y = y * PIXEL
        self.orientation = orientation
        self.frect = self.sprite.get_frect(center=(self.x, self.y))
        self.color = BACKGROUND
        self.sprite.fill(self.color)

        self.length = length

    def draw_ship():
        pass
