from random import randint

import pygame as pg

# Псевдонимы типов:
Pointer = tuple[int, int]
Color = tuple[int, int, int]

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Color = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color: Color | None = None) -> None:
        self.position: Pointer = (
            (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        )
        self.body_color: Color | None = body_color

    def draw(self) -> None:
        """Отрисовывает объект на игровом поле."""
        raise NotImplementedError(
            'draw метод должен быть переопределен в дочернем классе'
        )


class Apple(GameObject):
    """Дочерний класс яблока."""

    def __init__(
            self, occupied_positions: list[Pointer] | None = None,
            body_color: Color = APPLE_COLOR
    ) -> None:
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(
            self, occupied_positions: list[Pointer] | None = None
    ) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if (
                occupied_positions is None
                or self.position not in occupied_positions
            ):
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = (pg.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс питона."""

    def __init__(self, body_color: Color = SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.reset()

    def get_head_position(self) -> Pointer:
        """Возвращает текущие координаты головного конца"""
        return self.positions[0]

    def move(self) -> None:
        """Перемещает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        next_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        next_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (next_x, next_y)
        self.positions.insert(0, new_head)
        if self.length < len(self.positions):
            self.positions.pop()

    def reset(self) -> None:
        """питон врезается сам в себя и сбрасывается"""
        self.length: int = 1
        self.positions: list[Pointer] = [
            (
                (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
            )
        ]
        self.direction: Pointer = RIGHT
        self.next_direction: Pointer | None = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовка головы змейки, тела и затирание хвостового сегмента"""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object: Snake) -> None:
    """функция снятия нажатий клавиатуры"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры"""
    # Инициализация PyGame:
    pg.init()
    # Экземпляры классов.
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # наступаем головой на яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_positions=snake.positions)

        # Столкновение змейки с самой собой.
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
