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

def game_mood(screen):
    font = pygame.font.Font(None, 36)
    mode = ""

    background = pygame.image.load("pong_fond.png").convert()
    background = pygame.transform.scale(background, (WIDHT, HEIGHT))

    while mode == "":
        screen.blit(background, (0,0))

        text1 = font.render("Chose the game mode : ", True, COLOR)
        text2 = font.render("Play with a Friend", True, COLOR)
        text3 = font.render("Play vs AI", True, COLOR)
        
        # Adding text on the screen
        screen.blit(text1, (WIDHT // 2 - text1.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(text2, (WIDHT // 2 - text2.get_width() // 2, HEIGHT // 2))
        screen.blit(text3, (WIDHT // 3 - text3.get_width() // 2 + 50))

        # Draw the buttons 
        pygame.draw.rect(screen, (0, 255, 0), (WIDHT // 2 - 150, HEIGHT // 2 - 20, 300, 40))
        pygame.draw.rect(screen, (0, 255, 0), (WIDHT // 2 - 150, HEIGHT // 2 + 30, 300, 40))

        text_button1 = font.render("Play with a Friend", True, WHITE_COULEUR)
        screen.blit(text_button1, (WIDHT // 2 - text_button1.get_width() // 2, HEIGHT // 2 - 10))
        text_button2 = font.render("Play vs AI", True, WHITE_COULEUR)
        screen.blit(text_button2, (WIDHT // 2 - text_button2.get_width() // 2, HEIGHT // 2 + 40))

        pygame.display.flip()

        # Configuration about the buttons and text whe coming for the first time 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "friend"
                elif event.key == pygame.K_2:
                    mode = "AI"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if (WIDHT // 2 - 150 <= mouse_position[0] <= WIDHT // 2 + 150) and (HEIGHT // 2 - 20 <= mouse_position[1] <= HEIGHT // 2 + 20):
                    mode = "Friend"
                elif (WIDHT // 2 - 150 <= mouse_position[0] <= WIDHT // 2 + 150) and (HEIGHT // 2 + 30 <= mouse_position[1] <= HEIGHT // 2 + 70 ):
                    mode = "AI"

    return mode

def initialization_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDHT, HEIGHT))
    pygame.display.set_caption("Ping Pong Game")
    return screen