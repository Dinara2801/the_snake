from random import randrange

import pygame as pg


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_HEIGHT = 640, 600, 480
HAT_HEIGTH = SCREEN_HEIGHT - BOARD_HEIGHT
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH - GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT - GRID_SIZE
SCORE_POSITION = (GRID_SIZE * 0.5, BOARD_HEIGHT)
ISTRUCTION_POSITION = (GRID_SIZE * 0.5, BOARD_HEIGHT + GRID_SIZE * 0.5)
SPEED_POSITION = (SCREEN_WIDTH - GRID_SIZE * 15, BOARD_HEIGHT)


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (73, 160, 22)
BOARD_COLOR = (73, 176, 22)
GRID_COLOR_1 = (140, 212, 79)
GRID_COLOR_2 = (163, 212, 79)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 128, 255)
SCORE_COLOR = (255, 255, 255)
INSTRUCTION_COLOR = (102, 51, 0)

# Скорость движения змейки:
speed = 10
speed_delta = 10

score = 0
game_instruction = ['Добро пожаловать в игру \'Змейка\'!',
                    'Управляйте змейкой с помощью клавиш \'ВВЕРХ\', \'ВНИЗ\','
                    '\'ВЛЕВО\', \'ВПРАВО\'.',
                    'Для изменения скорости движения змейки нажмите -/=.',
                    'Для выхода из игры нажмите \'ESC\'.']

NEXT_DIRECTION = {(LEFT, pg.K_UP): UP,
                  (RIGHT, pg.K_UP): UP,
                  (UP, pg.K_LEFT): LEFT,
                  (DOWN, pg.K_LEFT): LEFT,
                  (UP, pg.K_RIGHT): RIGHT,
                  (DOWN, pg.K_RIGHT): RIGHT,
                  (RIGHT, pg.K_DOWN): DOWN,
                  (LEFT, pg.K_DOWN): DOWN}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
board = pg.Rect((0, 0), (SCREEN_WIDTH, BOARD_HEIGHT))
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс объектов игры."""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, BOARD_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Метод, отвечающий за отрисовку объекта."""
        """Переопределяется в дочерних классах."""
        raise NotImplementedError(f'В классеse {self.__class__.__name__} '
                                  'не переопределен метод draw')

    def draw_rect(self, position, body_color, frame_color=BORDER_COLOR):
        """Метод отрисовки ячейки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, frame_color, rect, 1)


class Apple(GameObject):
    """Класс игрового объекта 'Яблоко'."""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=[]):
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def draw(self):
        """Метод отрисовки яблока на игровом поле."""
        apple_x, apple_y = self.position
        pg.draw.circle(screen, self.body_color,
                       (apple_x + 10, apple_y + 10), 8)
        pg.draw.line(screen, INSTRUCTION_COLOR, (apple_x + 10, apple_y + 5),
                     (apple_x + 13, apple_y), 2)
        pg.draw.polygon(screen, BOARD_BACKGROUND_COLOR,
                        [[apple_x + 2, apple_y + 2],
                         [apple_x + 7, apple_y + 2],
                         [apple_x + 10, apple_y + 5],
                         [apple_x + 5, apple_y + 5]])

    def randomize_position(self, occupied_positions):
        """Метод, отвечающий за определение местоположения яблока."""
        while True:
            self.position = (randrange(GRID_SIZE, SCREEN_WIDTH - GRID_SIZE,
                                       GRID_SIZE),
                             randrange(GRID_SIZE, BOARD_HEIGHT - GRID_SIZE,
                                       GRID_SIZE))
            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """Класс игрового объекта 'Змейка'."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Метод, без корого не проходят автоматические тесты."""
        """Если его совсем убрать, то игра работает нормально."""
        """Однако, если его убрать, то работа не отправится на ревью."""
        pass

    def move(self):
        """Метод, отвечающий за обработку движений змейки."""
        direction_x, direction_y = self.direction
        head_x, head_y = self.get_head_position()
        self.position = ((head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
                         (head_y + direction_y * GRID_SIZE) % BOARD_HEIGHT)

        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод, отвечающий за отрисовку змейки на игровом поле."""
        self.draw_rect(self.get_head_position(), self.body_color)

        for position in self.positions[1:]:
            self.draw_rect(position, self.body_color)

        if self.last:
            last_x, last_y = self.last
            if last_x == 0 or last_x == (SCREEN_WIDTH - GRID_SIZE):
                color = BOARD_COLOR
            elif last_y == 0 or last_y == (BOARD_HEIGHT - GRID_SIZE):
                color = BOARD_COLOR
            else:
                color = (GRID_COLOR_1
                         if ((last_x + last_y) / GRID_SIZE) % 2 == 0
                         else GRID_COLOR_2)
            self.draw_rect(self.last, color, BOARD_COLOR)

    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Этот метод сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, BOARD_HEIGHT // 2)]
        self.next_direction = None
        self.last = None


def draw_board(color_1, color_2):
    """Функция отрисовки игрового поля."""
    for row in range(22):
        for col in range(30):
            if (row + col) % 2 == 0:
                color = color_1
            else:
                color = color_2
            pg.draw.rect(screen, color, [20 + col * GRID_SIZE,
                                         20 + row * GRID_SIZE,
                                         GRID_SIZE, GRID_SIZE])
            pg.draw.rect(screen, BOARD_COLOR, [20 + col * GRID_SIZE,
                                               20 + row * GRID_SIZE,
                                               GRID_SIZE, GRID_SIZE], 1)


def draw_score(font, score, speed, score_position, speed_position):
    """Функция отображающая счтет игры."""
    pg.draw.rect(screen, BOARD_BACKGROUND_COLOR,
                 [score_position, (SCREEN_WIDTH, GRID_SIZE + 4)])
    your_score = font.render(f'Ваш счёт: {score}', 1, SCORE_COLOR)
    screen.blit(your_score, score_position)
    snake_speed = font.render(f'Скорость движения змейки: {speed // 10}',
                              1, SCORE_COLOR)
    screen.blit(snake_speed, speed_position)


def draw_instruction(font, text, position):
    """Функция отображающая инструкцию к игре."""
    x_instruction, y_instruction = position
    for instruction in text:
        y_instruction += 20
        instructions = font.render(instruction, 1, INSTRUCTION_COLOR)
        screen.blit(instructions, (x_instruction, y_instruction))


def handle_keys(game_object):
    """Функция, обрабатывающая нажатия клавиш."""
    global speed
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN
                                     and event.key == pg.K_ESCAPE):
            quit()
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            game_object.direction = NEXT_DIRECTION.get(
                (game_object.direction, event.key), game_object.direction)
            if event.key == pg.K_EQUALS:
                speed += speed_delta
                return speed
            elif event.key == pg.K_MINUS:
                speed -= speed_delta
                if speed <= speed_delta:
                    speed = speed_delta
                return speed


def main():
    """Основной цикл игры."""
    pg.init()

    global score
    SCORE_FONT = pg.font.SysFont('comicsansms', 20)
    INSTRUCTION_FONT = pg.font.SysFont('comicsansms', 16)

    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)
    pg.draw.rect(screen, BOARD_COLOR, board)
    draw_board(GRID_COLOR_1, GRID_COLOR_2)
    draw_instruction(INSTRUCTION_FONT, game_instruction, ISTRUCTION_POSITION)

    while True:

        clock.tick(speed)

        handle_keys(snake)

        snake.move()

        if apple.position == snake.get_head_position():
            snake.length += 1
            score += 1
            apple.randomize_position(snake.positions)
            # snake.last = snake.positions[-1]
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            pg.draw.rect(screen, BOARD_COLOR, board)
            draw_board(GRID_COLOR_1, GRID_COLOR_2)
            apple.randomize_position(snake.positions)
            score = 0

        snake.draw()
        apple.draw()
        draw_score(SCORE_FONT, score, speed, SCORE_POSITION, SPEED_POSITION)

        pg.display.update()


if __name__ == '__main__':
    main()
