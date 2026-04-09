import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()


class Dino:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.width = 40
        self.height = 60
        self.jump = False
        self.jump_count = 12
        self.jump_counter_total = 0  

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height))

    def update(self):
        if self.jump:
            if self.jump_count >= -12:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.3 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 12


class Obstacle:
    def __init__(self, x, size, speed, color):
        self.x = x
        self.y = 330 - size
        self.size = size
        self.speed = speed
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def update(self):
        self.x -= self.speed



def create_random_obstacle():
    size = random.choice([20, 30, 40, 50])    
    speed = random.choice([5, 7, 9])          
    color = random.choice([(255,0,0), (0,0,255), (255,165,0)])  
    return Obstacle(850, size, speed, color)


dino = Dino()
obstacles = []
score = 0
run = True

while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not dino.jump:
        dino.jump = True
        dino.jump_counter_total += 1
        print("Прыжков:", dino.jump_counter_total)  


    dino.update()


    if len(obstacles) < 3:
        if random.randint(1, 40) == 1:
            obstacles.append(create_random_obstacle())

 
    for obs in obstacles[:]:
        obs.update()
        if obs.x < -50:
            obstacles.remove(obs)
            score += 1

    
        if (dino.x < obs.x + obs.size and
            dino.x + dino.width > obs.x and
            dino.y < obs.y + obs.size and
            dino.y + dino.height > obs.y):
            print("GAME OVER")
            run = False


    if score >= 100:
        win.fill((0, 255, 0))  
    else:
        win.fill((200, 200, 200))

    dino.draw(win)
    for obs in obstacles:
        obs.draw(win)

    pygame.display.update()

pygame.quit()