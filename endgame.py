import pygame
from settings import *
from button import Button

class Endgame:
    def __init__(self, screen, message, row, col) -> None:
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 60)
        
        self.cannon_move_frames = [pygame.image.load(f"{CANNON_MOVE}{i}.png").convert_alpha() for i in range(1, 4)]
        self.cannon_shoot_frames = [pygame.image.load(f"{CANNON_SHOOT}{i}.png").convert_alpha() for i in range(1, 9)]
        self.cannon_ball_frames = [pygame.image.load(f"{CANNON_BALL}{i}.png").convert_alpha() for i in range(1, 3)]

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 10

        self.cannon_x = -250
        self.cannon_y = 90
        self.cannon_speed = 5

        self.message = message

        self.ball_frame_index = 0
        self.ball_x = None
        self.ball_y = self.cannon_y + 40
        self.ball_speed = 6

        self.show_letters = []
        self.next_letter_index = 0
        self.next_letter_x = None
        self.letter_y = 140
        self.letter_interval = 45

        self.cannon_in_position = False
        self.shot_animation_done = False
        self.shooting = False
        self.shot_frame_index = 0

        self.retry_button = Button("assets/button/button.png", 150, 250, "Retry")
        self.quit_button = Button("assets/button/button.png", 450, 250, "Quit")

        self.x_tile = col * PIXEL
        self.y_tile = row * PIXEL

    def run(self):
        running = True
        result = None
        
        while running:
            pygame.draw.rect(self.screen, (0, 0, 0), (0,0, WINDOW_WIDTH, WINDOW_HEIGHT/3))
            pygame.draw.rect(self.screen, (179, 179, 204), (0, WINDOW_HEIGHT/3, WINDOW_WIDTH, (WINDOW_HEIGHT/3)*2))
            pygame.draw.rect(self.screen, (0, 0, 0), (0, (WINDOW_HEIGHT/3)*2, WINDOW_WIDTH, WINDOW_HEIGHT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = "quit"
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.retry_button.isClicked(mouse_x, mouse_y):
                        result = "retry"
                        running = False
                    elif self.quit_button.isClicked(mouse_x, mouse_y):
                        result = "quit"
                        running = False
            
            # Movement of the cannon until it is in the final position
            if not self.cannon_in_position:
                self.cannon_x += self.cannon_speed
                if self.cannon_x >= 30:
                    self.cannon_x = 30
                    self.cannon_in_position = True
                    self.shooting = True

                # Update movement frame
                self.frame_timer += 1
                if self.frame_timer >= self.frame_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.cannon_move_frames)
                    self.frame_timer = 0

                self.screen.blit(self.cannon_move_frames[self.current_frame], (self.cannon_x, self.cannon_y))
            
            # If the cannon is in position, start shooting
            elif self.shooting and not self.shot_animation_done:
                # Show current shot frame
                if self.shot_frame_index < len(self.cannon_shoot_frames):
                    self.screen.blit(self.cannon_shoot_frames[self.shot_frame_index], (self.cannon_x, self.cannon_y))

                    # Initialize ball on frame 4
                    if self.shot_frame_index == 3 and self.ball_x is None:
                        self.ball_x = self.cannon_x + 100
                        self.next_letter_x = self.ball_x + 100

                    self.frame_timer += 1
                    if self.frame_timer >= self.frame_delay:
                        self.shot_frame_index += 1
                        self.frame_timer = 0
                else:
                    # Freeze on last frame
                    self.screen.blit(self.cannon_shoot_frames[-1], (self.cannon_x, self.cannon_y))
                    self.shot_animation_done = True
                    self.shooting = False

            # If the cannon has finished shooting, animate the ball
            elif self.shot_animation_done:

                # Keep the last cannon frame on the screen
                self.screen.blit(self.cannon_shoot_frames[-1], (self.cannon_x, self.cannon_y))

                # Movement of the ball if it has already been fired
                if self.ball_x is not None:
                    # Animate the ball
                    self.ball_frame_index = (self.ball_frame_index + 1) % len(self.cannon_ball_frames)
                    self.screen.blit(self.cannon_ball_frames[self.ball_frame_index], (self.ball_x, self.ball_y))

                    # Add letter from the message if it has reached the position
                    if self.ball_x >= self.next_letter_x and self.next_letter_index < len(self.message):
                        letter = self.message[self.next_letter_index]
                        text_surface = self.font.render(letter, True, (255, 255, 255))
                        letter_x = self.next_letter_x + 40
                        self.show_letters.append((text_surface, letter_x))
                        self.next_letter_index += 1
                        self.next_letter_x += self.letter_interval

                    # Move the ball
                    self.ball_x += self.ball_speed

                    # Remove the ball if it goes off screen
                    if self.ball_x > WINDOW_WIDTH + 50:
                        self.ball_x = None 

                # Show all letters that have appeared
                for i, (surf, x) in enumerate(self.show_letters):
                    self.screen.blit(surf, (x, self.letter_y))

                if self.next_letter_index >= len(self.message):
                    self.retry_button.draw(self.screen)
                    self.quit_button.draw(self.screen)


            pygame.display.flip()
            self.clock.tick(100)
        return result