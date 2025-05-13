import pygame

from settings import *

class Token(pygame.sprite.Sprite):
    def __init__(self, img, x, y, imgList = None, frameNumber = None):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.imageList = imgList
        self.frameNumber = frameNumber
        
    def animate(self, screen):
        if self.imageList is not None and self.frameNumber is not None:
            for frame in range(1, self.frameNumber + 1):
                TOKEN_FRAME = f"{self.imageList}{frame}.png"
                tile = pygame.image.load(TOKEN_FRAME).convert_alpha()
                tile = pygame.transform.scale(tile, (PIXEL, PIXEL))
                screen.blit(tile, (self.x, self.y))
                pygame.display.update()
                pygame.time.delay(100)
            
        
    def draw(self, screen):
        if self.imageList is None:
            screen.blit(self.image, (self.x, self.y))