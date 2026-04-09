import pygame
pygame.init()

# Окно
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Ping Pong")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Игроки и мяч
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 80
BALL_SIZE = 20

player1 = pygame.Rect(20, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
player2 = pygame.Rect(WIDTH-40, HEIGHT//2 - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

# Скорости
player_speed = 5
ball_speed_x = 4
ball_speed_y = 4

background = pygame.Surface((WIDTH, HEIGHT))
background.fill((0, 150, 200))  # голубой фон

clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # Управление игроком 1 (W/S)
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= player_speed
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += player_speed

    # Управление игроком 2 (UP/DOWN)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= player_speed
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += player_speed

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскок от стен
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Столкновение с игроками
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1

    # Если мяч улетел за пределы — возвращаем в центр
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x = WIDTH//2
        ball.y = HEIGHT//2
        ball_speed_x *= -1

    # Рисуем
    WIN.blit(background, (0, 0))
    pygame.draw.rect(WIN, BLACK, player1)
    pygame.draw.rect(WIN, BLACK, player2)
    pygame.draw.ellipse(WIN, WHITE, ball)

    pygame.display.update()

pygame.quit()