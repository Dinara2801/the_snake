from random import randrange
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс объектов игры."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод, отвечающий за отрисовку объекта."""
        """Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс игрового объекта 'Яблоко'."""

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод отрисовки яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @classmethod
    def randomize_position(cls):
        """Метод класса отвечающий за определение местоположения яблокаю"""
        return (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE))


class Snake(GameObject):
    """Класс игрового объекта 'Змейка'."""

    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        super().__init__()
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод, который обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Метод, отвечающий за обработку движений змейки."""
        x, y = self.get_head_position()
        new_x = x + self.direction[0] * GRID_SIZE
        if new_x >= SCREEN_WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = SCREEN_WIDTH - GRID_SIZE

        new_y = y + self.direction[1] * GRID_SIZE
        if new_y >= SCREEN_HEIGHT:
            new_y = 0
        elif new_y < 0:
            new_y = SCREEN_HEIGHT - GRID_SIZE

        new_head_position = (new_x, new_y)
        self.positions.insert(0, new_head_position)

        if apple.position == self.get_head_position():
            self.length += 1
            self.last = self.positions[-1]
            apple.position = apple.randomize_position()
            if apple.position in self.positions:
                apple.position = apple.randomize_position()
        if len(self.positions) > self.length:
            self.positions.pop()

        if self.get_head_position() in self.positions[1:]:
            self.reset()

    def draw(self):
        """Метод, отвечающий за отрисовку змейки на игровом поле."""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Этот метод сбрасывает змейку в начальное состояние."""
        head_position = self.get_head_position()
        self.length = 1
        self.positions = []
        self.positions.append(head_position)


def handle_keys(game_object):
    """Функция, обрабатывающая нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры"""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move(apple)

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
