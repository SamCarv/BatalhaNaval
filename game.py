import random
from settings import *
from battleship import Battleship, Orientation, set_battleship
from battletoken import Token
from button import Button
from endgame import Endgame
import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Batalha Naval")
        self.clock = pygame.time.Clock()
        self.turn = True

        background_image_size = 352
        background_image_row = background_image_size // PIXEL
        background_image_col = background_image_size // PIXEL

        self.background = pygame.image.load(GAME_BACKGROUND).convert()
        self.background = pygame.transform.scale(
            self.background,
            ((23 * PIXEL), (22 * PIXEL)),
        )

        self.player_background = pygame.image.load(PLAYER_BACKGROUD).convert()
        self.player_background = pygame.transform.scale(
            self.player_background,
            ((background_image_row * PIXEL), (background_image_col * PIXEL)),
        )

        self.coop_background = pygame.image.load(COOP_BACKGROUND).convert()
        self.coop_background = pygame.transform.scale(
            self.coop_background,
            (((background_image_row * PIXEL)), (background_image_col * PIXEL)),
        )

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.battleship_grid = [row[:] for row in self.grid[: len(self.grid) // 2]]
        self.battleships_sprites = pygame.sprite.Group()

        self.bot_battleship_sprites = pygame.sprite.Group()

        self.bot_battleship_grid = [
            row[:] for row in self.grid[(len(self.grid) // 2) + 1 :]
        ]

        print(len(self.battleship_grid), len(self.bot_battleship_grid))

        self.player_view_grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

        def generate_random_battleship(sprite, size):
            while True:
                orientation = random.choice(list(Orientation))
                if orientation == Orientation.HORIZONTAL:
                    x = random.randint(1, 10 - size)
                    y = random.randint(1, len(self.battleship_grid) - 2)
                    if all(self.battleship_grid[y][x + i] == 0 for i in range(size)):
                        for i in range(size):
                            self.battleship_grid[y][x + i] = 1
                        return Battleship(sprite, size, x, y, orientation)
                else:
                    x = random.randint(1, 10 - 1)
                    y = random.randint(1, len(self.battleship_grid) - size)
                    if all(self.battleship_grid[y + i][x] == 0 for i in range(size)):
                        for i in range(size):
                            self.battleship_grid[y + i][x] = 1
                        return Battleship(sprite, size, x, y, orientation)

        def generate_random_bot_battleship(sprite, size):
            while True:
                orientation = random.choice(list(Orientation))
                if orientation == Orientation.HORIZONTAL:
                    x = random.randint(13, 22 - size)
                    y = random.randint(1, len(self.bot_battleship_grid) - 1)
                    if all(
                        self.bot_battleship_grid[y][x + i] == 0 for i in range(size)
                    ):
                        for i in range(size):
                            self.bot_battleship_grid[y][x + i] = 1
                        return Battleship(sprite, size, x, y, orientation)
                else:
                    x = random.randint(13, 22 - 1)
                    y = random.randint(1, len(self.bot_battleship_grid) - size)
                    if all(
                        self.bot_battleship_grid[y + i][x] == 0 for i in range(size)
                    ):
                        for i in range(size):
                            self.bot_battleship_grid[y + i][x] = 1
                        return Battleship(sprite, size, x, y, orientation)

        self.battleship_1 = generate_random_battleship(BATTLE_SHIP1X2, 2)
        self.battleship_2 = generate_random_battleship(BATTLE_SHIP1X4, 4)
        self.battleship_3 = generate_random_battleship(BATTLE_SHIP1X5, 5)

        self.battleships_sprites.add(
            self.battleship_1, self.battleship_2, self.battleship_3
        )

        self.bot_battleship_1 = generate_random_bot_battleship(BATTLE_SHIP1X2, 2)
        self.bot_battleship_2 = generate_random_bot_battleship(BATTLE_SHIP1X4, 4)
        self.bot_battleship_3 = generate_random_bot_battleship(BATTLE_SHIP1X5, 5)

        self.bot_battleship_sprites.add(
            self.bot_battleship_1, self.bot_battleship_2, self.bot_battleship_3
        )

        set_battleship(self.battleships_sprites, self.battleship_grid)

        self.screen.blit(self.background, (0,0))

        self.radar_button = Button(RADAR_BUTTON, 280, 400, "Radar")
        self.radar_button.draw(self.screen)

        self.bot_battleship_grid_already_played = [
            row[:] for row in self.grid[(len(self.grid) // 2) :]
        ]
        self.bot_view = [[None for _ in range(COLS)] for _ in range(ROWS)]

        for battleship in self.bot_battleship_sprites:
            if battleship.orientation == Orientation.HORIZONTAL:
                for i in range(battleship.size):
                    self.bot_battleship_grid[battleship.y][battleship.x + i] = 1
            else:
                for i in range(battleship.size):
                    self.bot_battleship_grid[battleship.y + i][battleship.x] = 1

    def run(self):
        running = True
        action = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Bot Turn

                if self.turn == False:
                    # Col - 13 até 22
                    # Row - 1 até 10
                    bot_x = random.randint(1, 10)
                    bot_y = random.randint(13, 22)

                    print(bot_x, bot_y)

                    while (
                        self.bot_battleship_grid_already_played[bot_x][bot_y] != 2
                        or self.bot_battleship_grid_already_played[bot_x][bot_y] == 1
                    ):

                        if self.bot_battleship_grid[bot_x][bot_y] == 0:
                            self.bot_battleship_grid_already_played[bot_x][bot_y] = 2
                            self.bot_view[bot_x][bot_y] = 0
                            

                            missToken = Token(
                                TOKEN_BLUE_MISS,
                                bot_y * PIXEL,
                                bot_x * PIXEL,
                                TOKEN_BLUE_MISS_LIST,
                                13,
                            )
                            
                            missToken.animate(self.screen)
                            
                            self.turn = True

                        if self.bot_battleship_grid[bot_x][bot_y] == 1:
                            print("Achei o barco")

                            self.bot_view[bot_x][bot_y] = 1
                            
                            tokenHit = Token(
                                TOKEN_BLUE_HIT,
                                bot_y * PIXEL,
                                bot_x * PIXEL,
                                TOKEN_BLUE_HIT_LIST,
                                13,
                            )
                            tokenHit.animate(self.screen)

                            self.turn = True
                            break

                # print(bot_x, bot_y)

                # Player Turn
                if self.turn:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        row = mouse_y // (PIXEL)
                        col = mouse_x // (PIXEL)

                        if self.radar_button.isClicked(mouse_x, mouse_y):

                            for frame in range(1, 360):
                                TOKEN_FRAME = f"{RADAR_LIST}{frame}.png"
                                tile = pygame.image.load(TOKEN_FRAME).convert_alpha()
                                tile = pygame.transform.scale(
                                    tile, (10 * PIXEL, 10 * PIXEL)
                                )
                                self.screen.blit(tile, (1 * PIXEL, 1 * PIXEL))
                                pygame.display.update()
                                pygame.time.delay(5)

                            validChoice = False
                            while not validChoice:
                                x = random.randint(0, 9)
                                y = random.randint(0, 9)
                                if self.battleship_grid[x][y] == 1 and self.player_view_grid[x][y] is None:
                                    validChoice = True

                            coordinate = f"({y}, {x})"
                            font = pygame.font.SysFont(None, 32, bold=True)
                            text = font.render(coordinate, True, (0,0,0))
                            self.screen.blit(text, (330, 370))

                        if (
                            row == 0
                            or col == 0
                            or col == 12
                            or col == 11
                            or row >= 11
                            or col >= 12
                        ):
                            continue

                        if self.player_view_grid[row][col] is not None:
                            continue

                        if self.battleship_grid[row][col] == 0:
                            self.turn = False

                            self.grid[row][col] = 0
                            self.player_view_grid[row][col] = 0

                            token = Token(
                                TOKEN_GREEN_MISS,
                                col * PIXEL,
                                row * PIXEL,
                                TOKEN_GREEN_MISS_LIST,
                                3,
                            )
                            token.animate(self.screen)

                        elif self.battleship_grid[row][col] == 1:
                            self.turn = False

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
                                        hitToken = Token(
                                            TOKEN_GREEN_HIT,
                                            col * PIXEL,
                                            row * PIXEL,
                                            TOKEN_GREEN_HIT_LIST,
                                            13,
                                        )
                                        hitToken.animate(self.screen)
                                        battleship.hit(col - battleship.x)

                                else:
                                    if (
                                        battleship.x == col
                                        and battleship.y
                                        <= row
                                        < battleship.y + battleship.size
                                    ):
                                        hitToken = Token(
                                            TOKEN_GREEN_HIT,
                                            col * PIXEL,
                                            row * PIXEL,
                                            TOKEN_GREEN_HIT_LIST,
                                            13,
                                        )
                                        hitToken.animate(self.screen)
                                        battleship.hit(row - battleship.y)

            self.screen.blit(self.player_background, (0, 0))
            self.screen.blit(self.coop_background, (384, 0))

            for battleship in self.battleships_sprites:
                if battleship.is_sunk():
                    battleship.draw(self.screen)

            for battleship in self.bot_battleship_sprites:
                if not battleship.is_sunk():
                    battleship.draw(self.screen)

            for row in range(ROWS):
                for col in range(COLS):
                    x = col * PIXEL
                    y = row * PIXEL

                    if self.player_view_grid[row][col] == 0:
                        tile = Token(TOKEN_GREEN_MISS, x, y)
                        tile.draw(self.screen)
                    elif self.bot_view[row][col] == 0:
                        tile = Token(TOKEN_BLUE_MISS, x, y)
                        tile.draw(self.screen)
                    elif self.player_view_grid[row][col] == 1:
                        tile = Token(TOKEN_GREEN_HIT, x, y)
                        tile.draw(self.screen)
                    elif self.bot_view[row][col] == 1:
                        tile = Token(TOKEN_BLUE_HIT, x, y)
                        tile.draw(self.screen)
            if all(ship.is_sunk() for ship in self.battleships_sprites):
                endgame_screen = Endgame(self.screen, "You Win!", row, col)
                action = endgame_screen.run()
            
            elif all(ship.is_sunk() for ship in self.bot_battleship_sprites):
                endgame_screen = Endgame(self.screen, "You Lose!", row, col)
                action = endgame_screen.run()

            if action == "retry":
                self.__init__()
                return
            elif action == "quit":
                running = False

            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()
