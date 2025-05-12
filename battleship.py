import pygame
from settings import *
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Battleship(pygame.sprite.Sprite):
    def __init__(self, img, size, x, y, orientation):
        super().__init__()
        self.image = img
        self.size = size
        self.x = x
        self.y = y
        self.position = (x, y)
        self.orientation = orientation
        self.length = len(img)
        self.hit_positions = [False] * self.length

    def hit(self, position):
        if position < 0 or position >= self.length:
            raise ValueError("Invalid position")
        self.hit_positions[position] = True

    def is_sunk(self):
        return all(self.hit_positions)
    
    def loadImage(path, size):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, size)
        return img
    
    def draw(self, screen):
        if self.orientation == Orientation.HORIZONTAL:
            for i in range(self.length):
                screen.blit(self.image[i], (self.position[0] + i * PIXEL, self.position[1]))
        else:
            for i in range(self.length):
                screen.blit(self.image[i], (self.position[0], self.position[1] + i * PIXEL))

    