from random import randint

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
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
    """Базовый класс для игровых объектов."""

    def __init__(self) -> None:
        """Инициализация игрового объекта."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка игрового объекта."""
        pass


class Apple(GameObject):
    """Класс яблока в игре."""

    def __init__(self):
        """Инициализация яблока с случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Установить яблоко на случайную позицию."""
        self.position = (
            (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
            (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        )

    def reset_position(self, positions):
        """Генерировать новую позицию яблока, избегая тела змейки."""
        new_position = None
        while new_position is None or new_position in positions:
            new_position = (
                (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            )
        self.position = new_position

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position,
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки в игре."""

    def __init__(self):
        """Инициализация змейки в центре экрана."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        # вынесем инициализацию в отдельный метод, чтобы избежать вызова
        # конструктора на уже созданном объекте при сбросе
        self.reset()

    def reset(self):
        """Установить начальные параметры змейки.

        Этот метод используется и внутри конструктора, и при сбросе игры.
        """
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Получить позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить змейку в направлении движения."""
        self.update_direction()
        head_x, head_y = self.positions[0]
        new_head = (
            int((head_x + self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH,
            int((head_y + self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовать змейку на экране."""
        for position in list(self.positions)[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработать события клавиатуры и изменить направление змейки."""
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
    """Основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.reset_position(snake.positions)
            apple.draw()
        elif snake.get_head_position() in list(snake.positions)[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.display.update()


if __name__ == '__main__':
    main()
