from settings import *
from battleship import Battleship, Orientation, set_battleship
from battletoken import Token
from button import Button
import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Batalha Naval")
        self.clock = pygame.time.Clock()

        background_image_size = 352
        background_image_row = background_image_size // PIXEL
        background_image_cow = background_image_size // PIXEL

        self.background = pygame.image.load(PLAYER_BACKGROUD).convert()
        self.background = pygame.transform.scale(
            self.background,
            ((background_image_row * PIXEL), (background_image_cow * PIXEL)),
        )

        self.coop_background = pygame.image.load(COOP_BACKGROUND).convert()
        self.coop_background = pygame.transform.scale(
            self.coop_background,
            (((background_image_row * PIXEL)), (background_image_cow * PIXEL)),
        )

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.battleship_grid = [row[:] for row in self.grid]
        self.battleships_sprites = pygame.sprite.Group()
        
        self.player_view_grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

        self.battleship_1 = Battleship(BATTLE_SHIP1X2, 2, 2, 4, Orientation.HORIZONTAL)
        self.battleship_2 = Battleship(BATTLE_SHIP1X4, 4, 5, 5, Orientation.VERTICAL)
        self.battleship_3 = Battleship(BATTLE_SHIP1X5, 5, 8, 4, Orientation.VERTICAL)
        self.battleships_sprites.add(self.battleship_1, self.battleship_2, self.battleship_3)
        set_battleship(self.battleships_sprites, self.battleship_grid)
        # x = 280 y = 400  limite 416
        self.radar_button = Button(RADAR_BUTTON, 280, 400, "Radar")
        self.radar_button.draw(self.screen)
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

                    if row == 0 or col == 0 or col == 12 or col == 11 or row>= 11:
                        continue

                    # if self.grid[row][col] == 0:
                    #     continue

                    if self.player_view_grid[row][col] is not None:
                        continue

                    if self.battleship_grid[row][col] == 0:
                        self.grid[row][col] = 0
                        self.player_view_grid[row][col] = 0
                        
                        token = Token(TOKEN_GREEN_MISS, col * PIXEL, row * PIXEL, TOKEN_GREEN_MISS_LIST, 14)
                        token.animate(self.screen)
                        
                    elif self.battleship_grid[row][col] == 1:
                        self.grid[row][col] = 1
                        self.player_view_grid[row][col] = 1

                        for battleship in self.battleships_sprites:
                            if battleship.orientation == Orientation.HORIZONTAL:
                                if (
                                    battleship.y == row
                                    and battleship.x
                                    <= col
                                    < battleship.x + battleship.size
                                ):
                                    hitToken = Token(TOKEN_GREEN_HIT, col * PIXEL, row * PIXEL, TOKEN_GREEN_HIT_LIST, 14)
                                    hitToken.animate(self.screen)
                                    battleship.hit(col - battleship.x)
                            else:
                                if (
                                    battleship.x == col
                                    and battleship.y
                                    <= row
                                    < battleship.y + battleship.size
                                ):
                                    hitToken = Token(TOKEN_GREEN_HIT, col * PIXEL, row * PIXEL, TOKEN_GREEN_HIT_LIST, 14)
                                    hitToken.animate(self.screen)
                                    battleship.hit(row - battleship.y)

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.coop_background, (384, 0))


            for battleship in self.battleships_sprites:
                if battleship.is_sunk():
                    battleship.draw(self.screen)

            for row in range(ROWS):
                for col in range(COLS):
                    x = col * PIXEL
                    y = row * PIXEL

                    if self.player_view_grid[row][col] == 0:
                        tile = Token(TOKEN_GREEN_MISS, x, y)
                        tile.draw(self.screen)
                    elif self.player_view_grid[row][col] == 1:
                        tile = Token(TOKEN_GREEN_HIT, x, y)
                        tile.draw(self.screen)

            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()
