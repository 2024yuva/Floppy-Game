import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
BIRD_WIDTH, BIRD_HEIGHT = 34, 24  # Bird size

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        # Prevent going out of bounds
        if self.y > HEIGHT - BIRD_HEIGHT:
            self.y = HEIGHT - BIRD_HEIGHT
            self.velocity = 0
        if self.y < 0:
            self.y = 0

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT))

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, 50, self.height))  # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + 150, 50, HEIGHT - self.height - 150))  # Bottom pipe

def main():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Flappy Bird')
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.move()
        bird.draw()

        for pipe in pipes:
            pipe.move()
            pipe.draw()

            if pipe.x + 50 < bird.x and not pipe.passed:
                score += 1
                pipe.passed = True

            if pipe.x < 0:  
                pipes.remove(pipe)
                pipes.append(Pipe())

        # Check for collisions
        if (bird.y > HEIGHT - BIRD_HEIGHT) or (bird.y < 0) or any(
            pipe.x < bird.x + BIRD_WIDTH and pipe.x + 50 > bird.x and 
            (bird.y < pipe.height or bird.y + BIRD_HEIGHT > pipe.height + 150) for pipe in pipes):
            print("Game Over! Final Score:", score)
            running = False

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
         main()
