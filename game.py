from settings import *
from battleship import Battleship, Orientation
import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Batalha Naval")
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load(PLAYER_BACKGROUD).convert()
        self.background = pygame.transform.scale(
            self.background, ((ROWS * PIXEL), (COLS * PIXEL))
        )

        self.grid = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        self.battleship_grid = [row[:] for row in self.grid]
        self.battleships_sprites = pygame.sprite.Group()

        self.battleship_1 = Battleship(BATTLE_SHIP1X2, 2, 2, 4, Orientation.HORIZONTAL)
        self.battleship_2 = Battleship(BATTLE_SHIP1X4, 4, 5, 5, Orientation.VERTICAL)
        self.battleships_sprites.add(self.battleship_1, self.battleship_2)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    row = mouse_y // (PIXEL)
                    col = mouse_x // (PIXEL)

                    if row == 0 or col == 0:
                        continue

                    if 0 <= row < ROWS and 0 <= col < COLS:
                        self.grid[row][col] *= -1

                    if self.battleship_grid[row][col] == 1:
                        self.grid[row][col] = 1
                    elif self.battleship_grid[row][col] == 0:
                        self.grid[row][col] = 0

                        for battleship in self.battleships_sprites:
                            if battleship.orientation == Orientation.HORIZONTAL:
                                if (
                                    battleship.y == row
                                    and battleship.x
                                    <= col
                                    < battleship.x + battleship.size
                                ):
                                    battleship.hit(col - battleship.x)
                            else:
                                if (
                                    battleship.x == col
                                    and battleship.y
                                    <= row
                                    < battleship.y + battleship.size
                                ):
                                    battleship.hit(row - battleship.y)

            self.screen.blit(self.background, (0, 0))

            # Render Game
            # Carregas barcos
            for battleship in self.battleships_sprites:
                size = battleship.size

                for i in range(size):
                    if battleship.orientation == Orientation.HORIZONTAL:
                        self.battleship_grid[battleship.y][battleship.x + i] = 0
                    else:
                        self.battleship_grid[battleship.y + i][battleship.x] = 0

                if battleship.is_sunk():
                    battleship.draw(self.screen)

            for row in range(ROWS):
                for col in range(COLS):
                    x = col * PIXEL
                    y = row * PIXEL

                    if self.grid[row][col] == -1:
                        tile = pygame.image.load(TOKEN_TRANSPARENT).convert_alpha()
                    elif self.grid[row][col] == 0:
                        tile = pygame.image.load(TOKEN_GREEN_HIT).convert_alpha()
                    elif self.grid[row][col] == 1:
                        tile = pygame.image.load(TOKEN_GREEN_MISS).convert_alpha()

                    self.screen.blit(tile, (x, y))

            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()
