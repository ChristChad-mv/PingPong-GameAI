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

def game_mode_choice(screen):
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
                    mode = "Friend"
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

def play_game(screen):
    mode = game_mode_choice(screen)
    clock = pygame.time.Clock() # Important one !!

    # We create players and balls here
    paddle_player_A = Paddle(COLOR, WIDTH_PADDLE, HEIGHT_PADDLE)
    paddle_player_A.rect.x = 0
    paddle_player_A.rect.y = (HEIGHT - HEIGHT_PADDLE) // 2

    paddle_player_B = Paddle(COLOR, WIDTH_PADDLE, HEIGHT_PADDLE)
    paddle_player_B.rect.x = WIDHT - WIDTH_PADDLE
    paddle_player_B.rect.y = (HEIGHT - HEIGHT_PADDLE) // 2

    ball = Ball(COLOR, 2 * BALL_RADUIS, 2 * BALL_RADUIS, BALL_RADUIS)
    ball.rect.centerx = WIDHT // 2
    ball.rect.centery = HEIGHT // 2

    # After defining the players and balls, We'll add all of them in the sprite
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(paddle_player_A)
    all_sprites_list.add(paddle_player_B)
    all_sprites_list.add(ball)

    running = True
    score_playerA, score_playerB = 0, 0

    while running:
        screen.fill(WHITE_COULEUR)
        pygame.draw.line(screen, COLOR, [WIDHT // 2, 0], [WIDHT // 2, HEIGHT], 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.get_pressed()
        if mode == "Friend":
            if keys[pygame.K_UP]:
                paddle_player_B.move_up(SPEED_PADDLE)
            if keys[pygame.K_DOWN]:
                paddle_player_B.move_down(SPEED_PADDLE)
            if keys[pygame.K_z]:
                paddle_player_A.move_up(SPEED_PADDLE)
            if keys[pygame.K_s]:
                paddle_player_A.move_down(SPEED_PADDLE)
        elif mode == "AI":
            pass
            """
            TODO : IMPLEMENTATION OF IA PLAYER
            """

        ball.update()

        if pygame.sprite.collide_mask(ball, paddle_player_A) or pygame.sprite.collide_mask(ball, paddle_player_B):
            ball.ball_bounce()

        if ball.rect.centerx > (WIDHT - BALL_RADUIS):
            (ball.rect.centerx, ball.rect.centery) = (WIDHT // 2, HEIGHT // 2)
            ball.velocity[0] *= -1
        
        all_sprites_list.draw(screen)

        pygame.font.init()
        font = pygame.font.Font(None, 74)
        text = font.render(str(score_playerA), 1, COLOR)
        screen.blit(text, (WIDHT // 4, 10))
        text = font.render(str(score_playerB), 1, COLOR)
        screen.blit(text, (3*WIDHT // 4, 10))

        pygame.display.flip()
        clock.tick(60) # 60 FPS for the screen

        if score_playerA == SCORE_MAX or score_playerB == SCORE_MAX:
            running = False
    pygame.quit()