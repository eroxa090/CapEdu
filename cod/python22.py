import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

dino_img = pygame.Surface((50, 50))
dino_img.fill((100, 200, 100))
dino_rect = dino_img.get_rect(bottomleft=(50, 350))
dino_y_vel = 0
gravity = 1
on_ground = True


obstacles = []
obstacle_timer = 0


score = 0
game_speed = 6
running = True
game_active = True

def create_obstacle():
    
    obstacle_type = random.choice(["small", "medium", "large"])
    if obstacle_type == "small":
        width, height, speed = 30, 30, 6
    elif obstacle_type == "medium":
        width, height, speed = 50, 40, 7
    else:
        width, height, speed = 70, 50, 8
    obstacle_rect = pygame.Rect(WIDTH, 350 - height, width, height)
    return (obstacle_rect, speed)

def reset_game():
   
    global obstacles, score, game_speed, dino_rect, dino_y_vel, on_ground, game_active
    obstacles = []
    score = 0
    game_speed = 6
    dino_rect.bottomleft = (50, 350)
    dino_y_vel = 0
    on_ground = True
    game_active = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground and game_active:
                dino_y_vel = -18
                on_ground = False
            elif event.key == pygame.K_r and not game_active:
                reset_game()

    screen.fill(WHITE)

    if game_active:
        
        dino_y_vel += gravity
        dino_rect.y += dino_y_vel
        if dino_rect.bottom >= 350:
            dino_rect.bottom = 350
            on_ground = True

        obstacle_timer += 1
        if obstacle_timer > 60:
            obstacle_timer = 0
            obstacles.append(create_obstacle())

        for obs in obstacles[:]:
            obs_rect, obs_speed = obs
            obs_rect.x -= obs_speed
            if obs_rect.right < 0:
                obstacles.remove(obs)
                score += 1
                if score % 5 == 0:
                    game_speed += 0.5  

        
            if dino_rect.colliderect(obs_rect):
                game_active = False

            pygame.draw.rect(screen, (200, 50, 50), obs_rect)

       
        screen.blit(dino_img, dino_rect)
        score_text = font.render(f"Счёт: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    else:
        over_text = font.render("Ты проиграл! Нажми R, чтобы перезапустить.", True, BLACK)
        screen.blit(over_text, (150, 150))
        score_text = font.render(f"Твой счёт: {score}", True, BLACK)
        screen.blit(score_text, (330, 200))

    pygame.display.update()
    clock.tick(60)