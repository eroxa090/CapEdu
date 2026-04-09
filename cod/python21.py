import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Paddle:
    def __init__(self, x):
        self.width = 15
        self.height = 100
        self.x = x
        self.y = HEIGHT // 2 - self.height // 2
        self.speed = 7

    def draw(self, win):
        pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up and self.y > 0:
            self.y -= self.speed
        elif not up and self.y + self.height < HEIGHT:
            self.y += self.speed

class Ball:
    def __init__(self):
        self.radius = 10
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_vel = random.choice([-5, 5])
        self.y_vel = random.choice([-3, 3])

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.y_vel *= -1

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def check_collision(self, paddle):
        """Проверка столкновения с платформой"""
        if (self.x - self.radius < paddle.x + paddle.width and
            self.x + self.radius > paddle.x and
            self.y > paddle.y and self.y < paddle.y + paddle.height):
            self.x_vel *= -1.1 
            self.y_vel *= 1.05  

def main():
    clock = pygame.time.Clock()
    left_paddle = Paddle(30)
    right_paddle = Paddle(WIDTH - 45)
    ball = Ball()

    left_score = 0
    right_score = 0
    font = pygame.font.SysFont("Arial", 36)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(up=True)
        if keys[pygame.K_s]:
            left_paddle.move(up=False)
        if keys[pygame.K_UP]:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            right_paddle.move(up=False)

        ball.move()
        ball.check_collision(left_paddle)
        ball.check_collision(right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        win.fill(BLACK)
        left_paddle.draw(win)
        right_paddle.draw(win)
        ball.draw(win)

        pygame.draw.aaline(win, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        score_text = font.render(f"{left_score} : {right_score}", True, WHITE)
        win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()