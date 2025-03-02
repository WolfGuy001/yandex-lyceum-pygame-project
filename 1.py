import pygame
import random
import sys


pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 50

# цвета
COLORS = {
    'background': (255, 255, 255),
    'snake': (0, 255, 0),
    'food': (255, 0, 0),
    'button': (200, 200, 200),
    'text': (0, 0, 0)
}

# шрифт
font = pygame.font.Font(None, 30)


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    return text_surface, text_rect


def start_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')

    selected_color = (0, 255, 0)
    selected_speed = 5
    colors = [(0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 0), (255, 0, 255)]
    speeds = [('Медленно', 5), ('Средне', 10), ('Быстро', 15)]

    while True:
        screen.fill(COLORS['background'])

        # выбор цвета
        color_text, color_rect = draw_text("Цвет змейки", COLORS['text'], SCREEN_WIDTH // 2, 100)
        screen.blit(color_text, color_rect)

        color_buttons = []
        for i, color in enumerate(colors):
            x = SCREEN_WIDTH // 2 - 165 + i * 70
            y = 130
            rect = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(screen, color, rect)
            if color == selected_color:
                pygame.draw.rect(screen, (0, 0, 0), rect, 3)
            color_buttons.append(rect)

        # выблр скорости
        speed_text, speed_rect = draw_text("Скорость игры", COLORS['text'], SCREEN_WIDTH // 2, 280)
        screen.blit(speed_text, speed_rect)

        speed_buttons = []
        for i, (name, speed) in enumerate(speeds):
            x = SCREEN_WIDTH // 2 - 200 + i * 140
            y = 320
            rect = pygame.Rect(x, y, 120, 40)
            pygame.draw.rect(screen, COLORS['button'], rect)
            text, text_rect = draw_text(name, COLORS['text'], x + 60, y + 20)
            screen.blit(text, text_rect)
            if speed == selected_speed:
                pygame.draw.rect(screen, (0, 0, 0), rect, 3)
            speed_buttons.append((rect, speed))

        # кнопка играть
        play_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 460, 200, 80)
        pygame.draw.rect(screen, COLORS['button'], play_rect)
        play_text, play_text_rect = draw_text("Играть", COLORS['text'], SCREEN_WIDTH // 2, 500)
        screen.blit(play_text, play_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for i, rect in enumerate(color_buttons):
                    if rect.collidepoint(mouse_pos):
                        selected_color = colors[i]

                for rect, speed in speed_buttons:
                    if rect.collidepoint(mouse_pos):
                        selected_speed = speed

                if play_rect.collidepoint(mouse_pos):
                    return selected_color, selected_speed


def game_over_screen(score):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        screen.fill(COLORS['background'])

        game_over_text, game_over_rect = draw_text(f"Игра окончена! Счёт: {score}",
                                                   COLORS['text'], SCREEN_WIDTH // 2, 220)
        screen.blit(game_over_text, game_over_rect)

        restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 270, 200, 40)
        pygame.draw.rect(screen, COLORS['button'], restart_rect)
        restart_text, restart_text_rect = draw_text("Начать сначала", COLORS['text'],
                                                    SCREEN_WIDTH // 2, 290)
        screen.blit(restart_text, restart_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    return


def game_loop(snake_color, speed):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    snake = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
    dx, dy = BLOCK_SIZE, 0
    food = [
        random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE),
        random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
    ]
    score = 0
    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        # логика игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK_SIZE, 0

        new_head = [snake[0][0] + dx, snake[0][1] + dy]
        snake.insert(0, new_head)

        if snake[0] == food:
            food = [
                random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE),
                random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)
            ]
            score += 1
        else:
            snake.pop()

        if (snake[0][0] < 0 or snake[0][0] >= SCREEN_WIDTH or
                snake[0][1] < 0 or snake[0][1] >= SCREEN_HEIGHT or
                snake[0] in snake[1:]):
            game_over = True

        screen.fill(COLORS['background'])

        for segment in snake:
            pygame.draw.rect(screen, snake_color,
                             (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        head = snake[0]
        eye_color = (255, 255, 255)
        eye_radius = BLOCK_SIZE // 8

        if dx > 0:  # вправо
            eye1_pos = (head[0] + BLOCK_SIZE * 3 // 4, head[1] + BLOCK_SIZE // 4)
            eye2_pos = (head[0] + BLOCK_SIZE * 3 // 4, head[1] + BLOCK_SIZE * 3 // 4)
        elif dx < 0:  # влево
            eye1_pos = (head[0] + BLOCK_SIZE // 4, head[1] + BLOCK_SIZE // 4)
            eye2_pos = (head[0] + BLOCK_SIZE // 4, head[1] + BLOCK_SIZE * 3 // 4)
        elif dy > 0:  # вниз
            eye1_pos = (head[0] + BLOCK_SIZE // 4, head[1] + BLOCK_SIZE * 3 // 4)
            eye2_pos = (head[0] + BLOCK_SIZE * 3 // 4, head[1] + BLOCK_SIZE * 3 // 4)
        else:  # вверх
            eye1_pos = (head[0] + BLOCK_SIZE // 4, head[1] + BLOCK_SIZE // 4)
            eye2_pos = (head[0] + BLOCK_SIZE * 3 // 4, head[1] + BLOCK_SIZE // 4)

        pygame.draw.circle(screen, eye_color, eye1_pos, eye_radius)
        pygame.draw.circle(screen, eye_color, eye2_pos, eye_radius)


        pygame.draw.rect(screen, COLORS['food'],
                         (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()
        clock.tick(speed)

    game_over_screen(score)


while True:
    snake_color, speed = start_menu()
    game_loop(snake_color, speed)