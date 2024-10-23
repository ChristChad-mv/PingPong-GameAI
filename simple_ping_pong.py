import pygame
import numpy as np

# Some important variables
COLOR = (255, 0, 0)
WHITE_COULEUR = (255, 255, 255)
WIDTH_PADDLE = 10
HEIGHT_PADDLE = 100
SPEED_PADDLE = 10
BALL_RADUIS = 10

SCORE_MAX = 5

# Screen variables
WIDHT = 840
HEIGHT = 600

# Create the basics element of the game
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height, raduis):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE_COULEUR)
        self.image.set_colorkey(WHITE_COULEUR)
        self.raduis = raduis
        self.width = width
        self.height = height
        self.velocity = [np.random.uniform(3, 6), np.random.uniform(-4, 4)]

        pygame.draw.circle(self.image, color, (self.width // 2, self.height // 2), self.raduis)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

    def ball_bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = np.random.uniform(-4, 5)

class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE_COULEUR)
        self.image.set_colorkey(WHITE_COULEUR)
        self.width = width
        self.height = height
        
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels

        # This test allows the ball to go out of the screen
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels

        if self.rect.y > (HEIGHT - self.height):
            self.rect.y = (HEIGHT - self.height)
