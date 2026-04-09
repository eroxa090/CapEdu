import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BG_COLOR = WHITE

jump_sound = pygame.mixer.Sound("sounds/jump.wav")
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
pygame.mixer.music.load("sounds/music.mp3")

dino = pygame.Rect(50, 300, 50, 50)
dino_vel_y = 0
gravity = 1

obstacles = []
obstacle_timer = 0

score = 0
jump_count = 0

game_speed = 6

font = pygame.font.SysFont("Arial", 24)


def start_menu():
  
    pygame.mixer.music.play(-1)

    while True:
        win.fill(WHITE)
        title = font.render("Dino Game", True, (0, 0, 0))
        start_text = font.render("Нажмите SPACE чтобы начать", True, (0, 0, 0))

        win.blit(title, (WIDTH//2 - 70, HEIGHT//2 - 40))
        win.blit(start_text, (WIDTH//2 - 180, HEIGHT//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


def spawn_obstacle():

    size = random.randint(30, 60)
    speed = game_speed + random.randint(0, 3)
    rect = pygame.Rect(WIDTH, 300 + (50 - size), size, size)
    return rect, speed



start_menu()
run = True

pygame.mixer.music.play(-1) 

while run:
    clock.tick(60)
    win.fill(BG_COLOR)

  
    if score % 50 == 0 and score != 0:
        game_speed += 0.01

 
    if score >= 100:
        BG_COLOR = GREEN

 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and dino.bottom >= 350:
                dino_vel_y = -17
                jump_sound.play()
                jump_count += 1
                print("Прыжков:", jump_count)

    dino_vel_y += gravity
    dino.y += dino_vel_y
    if dino.bottom >= 350:
        dino.bottom = 350

    pygame.draw.rect(win, (0, 0, 0), dino)

    obstacle_timer += 1
    if obstacle_timer > 60:
        obstacles.append(spawn_obstacle())
        obstacle_timer = 0

    for obs, speed in obstacles:
        obs.x -= speed
        pygame.draw.rect(win, (200, 0, 0), obs)

        
        if dino.colliderect(obs):
            hit_sound.play()
            pygame.time.delay(500)
            pygame.quit()
            quit()

    obstacles = [(o, s) for o, s in obstacles if o.x > -50]

    score += 1
    score_text = font.render(f"Счёт: {score}", True, (0, 0, 0))
    win.blit(score_text, (10, 10))

    pygame.display.update()