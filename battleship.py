import pygame
from settings import *
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class Battleship(pygame.sprite.Sprite):
    def __init__(self, img, size, x, y, orientation):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.size = size
        self.x = x
        self.y = y
        self.position = (x, y)
        self.orientation = orientation
        self.hit_positions = [False] * self.size

    def hit(self, position):
        if position < 0 or position >= self.size:
            raise ValueError("Invalid position")
        self.hit_positions[position] = True

    def is_sunk(self):
        return all(self.hit_positions)
    
    def draw(self, screen):
        if self.orientation == Orientation.HORIZONTAL:
            rotated_image = pygame.transform.rotate(self.image, 90)
            screen.blit(rotated_image, (self.x * PIXEL, self.y * PIXEL))
        else:
            screen.blit(self.image, (self.x * PIXEL, self.y * PIXEL))

def set_battleship(battleships_sprites, battleship_grid):
    for battleship in battleships_sprites:
        size = battleship.size
        for i in range(size):
            if battleship.orientation == Orientation.HORIZONTAL:
                battleship_grid[battleship.y][battleship.x + i] = 1
            else:
                battleship_grid[battleship.y + i][battleship.x] = 1
    