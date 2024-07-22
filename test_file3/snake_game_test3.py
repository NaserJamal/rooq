import pygame
import random


# snake_game
class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.cell_size = 20

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.fps = 10  # Control game speed
        self.reset()

    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.new_direction = None

    def generate_food(self):
        while True:
            food = (
                random.randint(
                    0, (self.width - self.cell_size) // self.cell_size
                ) * self.cell_size,
                random.randint(
                    0, (self.height - self.cell_size) // self.cell_size
                ) * self.cell_size
            )
            if food not in self.snake:
                return food

    def step(self):
        if self.game_over:
            return self.get_state(), 0, True

        # Update direction if a new one is set
        if self.new_direction:
            self.direction = self.new_direction
            self.new_direction = None

        # Move snake
        head = (
            self.snake[0][0] + self.direction[0] * self.cell_size,
            self.snake[0][1] + self.direction[1] * self.cell_size
        )
        self.snake.insert(0, head)

        # Check for collision with food
        if head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

        # Check for collision with walls or self
        if (head[0] < 0 or head[0] >= self.width or
                head[1] < 0 or head[1] >= self.height or
                head in self.snake[1:]):
            self.game_over = True

        return self.get_state(), self.score, self.game_over

    def change_direction(self, action):
        if action == 0 and self.direction != (0, 1):  # Up
            self.new_direction = (0, -1)
        elif action == 1 and self.direction != (0, -1):  # Down
            self.new_direction = (0, 1)
        elif action == 2 and self.direction != (1, 0):  # Left
            self.new_direction = (-1, 0)
        elif action == 3 and self.direction != (-1, 0):  # Right
            self.new_direction = (1, 0)

    def get_state(self):
        state = pygame.Surface((self.width, self.height))
        state.fill((0, 0, 0))

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(state, (0, 255, 0),
                             (*segment, self.cell_size, self.cell_size))

        # Draw food
        pygame.draw.rect(state, (255, 0, 0),
                         (*self.food, self.cell_size, self.cell_size))

        return pygame.surfarray.array3d(state).transpose((1, 0, 2))

    def render(self):
        self.screen.fill((0, 0, 0))

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (*segment, self.cell_size, self.cell_size))

        # Draw food
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (*self.food, self.cell_size, self.cell_size))

        pygame.display.flip()

    def close(self):
        pygame.quit()
