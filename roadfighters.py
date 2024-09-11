# ===================
# Imports
# ===================
import pygame
import random

# ===================
# Initialize Pygame
# ===================
pygame.init()

# ===================
# General Settings
# ===================
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CAR_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (255, 255, 0)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
obstacle_speed = 0
pygame.display.set_caption('Road Fighters')

# ===================
# Classes
# ===================

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 30])
        self.image.fill(CAR_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 40

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 30])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = 0 - 30

    def update(self):
        global obstacle_speed
        obstacle_speed = 5
        self.rect.y += obstacle_speed
        # self.rect.y += 5
        if self.rect.y > HEIGHT:
            self.rect.y = 0 - 30
            self.rect.x = random.randint(0, WIDTH - 50)

# ===================
# Functions
# ===================

def save_highscore(current_score):
    try:
        with open('highscoreRoadFighters.txt', 'r') as f:
            highscore = int(f.read())
    except:
        highscore = 0

    if current_score > highscore:
        with open('highscoreRoadFighters.txt', 'w') as f:
            f.write(str(current_score))

def read_highscore():
    try:
        with open('highscoreRoadFighters.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

def menu():
    font = pygame.font.Font(None, 36)
    highscore = read_highscore()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        SCREEN.fill(BLACK)

        highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
        SCREEN.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 - highscore_text.get_height() - 40))

        menu_text = font.render("1 - Single, 2 - AI Mode", True, WHITE)
        SCREEN.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - menu_text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            main()
        elif keys[pygame.K_2]:
            mainAI()

        pygame.display.update()

def victory_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 72)
    winner_text = font.render("You Win!", True, WHITE)
    text_position = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BLACK)
    screen.blit(winner_text, text_position)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    global CAR_COLOR, BACKGROUND_COLOR

    obstacle_speed = 5
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Road Fighters')

    score = 0 

    highscore = read_highscore()

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    car = Car()
    all_sprites.add(car)

    for i in range(5):
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    menu()

        all_sprites.update()

        hits = pygame.sprite.spritecollide(car, obstacles, False)
        if hits:
            save_highscore(score)
            running = False

        for obstacle in obstacles:
            if obstacle.rect.y == HEIGHT - 30:
                score += 10
                if score % 200 == 0:
                    obstacle_speed += 100
                    print(obstacle_speed)
        
        if score >= 500:
            save_highscore(score)
            victory_screen()
            running = False

        screen.fill(BACKGROUND_COLOR)
        
        highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(highscore_text, (WIDTH - 200, 10))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    menu()

def mainAI():
    car_pos = WIDTH // 2
    car_speed = 5
    obstacles = []
    obstacle_speed = 5
    score = 0
    
    obstacle_pos_y = 0
    obstacle_pos_x = random.randint(0, WIDTH - 50)
    obstacles.append((obstacle_pos_x, obstacle_pos_y))
    
    running = True
    while running:
        SCREEN.fill(BLACK)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        for index, (obs_x, obs_y) in enumerate(obstacles):
            pygame.draw.rect(SCREEN, WHITE, (obs_x, obs_y, 50, 50))
            obstacles[index] = (obs_x, obs_y + obstacle_speed)

        if obstacles[0][1] > HEIGHT:
            obstacles.pop(0)
            obstacle_pos_x = random.randint(0, WIDTH - 50)
            obstacles.append((obstacle_pos_x, 0))
            score += 1

        pygame.draw.rect(SCREEN, CAR_COLOR, (car_pos, HEIGHT - 60, 50, 50))

        nearest_obstacle = obstacles[0]
        distance_to_obstacle = HEIGHT - (nearest_obstacle[1] + 50)

        if distance_to_obstacle < 200:
            if nearest_obstacle[0] < car_pos:
                car_pos += car_speed
            else:
                car_pos -= car_speed
        else:  
            if car_pos < WIDTH // 2:
                car_pos += car_speed
            elif car_pos > WIDTH // 2:
                car_pos -= car_speed

        if car_pos < 0:
            car_pos = 0
        elif car_pos > WIDTH - 50:
            car_pos = WIDTH - 50

        pygame.display.update()

        car_rect = pygame.Rect(car_pos, HEIGHT - 60, 50, 50)
        obstacle_rect = pygame.Rect(obstacles[0][0], obstacles[0][1], 50, 50)
        if car_rect.colliderect(obstacle_rect):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    menu()

    print(f"Game Over! Score: {score}")

if __name__ == "__main__":
    menu()
