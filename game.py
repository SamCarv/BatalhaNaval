from settings import *
from battleship import Battleship, Orientation
import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Batalha Naval")
        self.clock = pygame.time.Clock()

        self.grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]

        self.battleship_grid = [row[:] for row in self.grid]

        self.battleships_sprites = pygame.sprite.Group()

        self.battleship_1 = Battleship(3, 1, 1, Orientation.HORIZONTAL)

        self.battleship_2 = Battleship(2, 4, 5, Orientation.VERTICAL)
        self.battleships_sprites.add(self.battleship_1, self.battleship_2)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    row = mouse_x // (PIXEL + 1)
                    col = mouse_y // (PIXEL + 1)

                    if 0 <= row < ROWS and 0 <= col < COLS:
                        self.grid[row][col] *= -1

                    if self.battleship_grid[row][col] == 0:
                        self.grid[row][col] = 0

            # Render Game
            # Carregas barcos
            for battleship in self.battleships_sprites:
                grid_x = battleship.x // (PIXEL + 1)
                grid_y = battleship.y // (PIXEL + 1)

                for i in range(battleship.length):
                    if battleship.orientation == Orientation.HORIZONTAL:
                        if 0 <= grid_x + i < ROWS:
                            self.battleship_grid[grid_x + i][grid_y] = 0
                    elif battleship.orientation == Orientation.VERTICAL:
                        if 0 <= grid_y + i < COLS:
                            self.battleship_grid[grid_x][grid_y + i] = 0

            for row in range(ROWS):
                for col in range(COLS):
                    x = row * (PIXEL + 1)
                    y = col * (PIXEL + 1)

                    color = BACKGROUND
                    if self.grid[row][col] == 1:
                        color = BACKGROUND
                    elif self.grid[row][col] == 0:
                        color = BATTLESHIP_COLOR
                    else:
                        color = WITHOUT_BATTLESHIP
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (x, y, PIXEL, PIXEL),
                    )

            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()
