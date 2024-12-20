"""
TRANNING AI
"""

import pygame
import numpy as np
import pickle
import matplotlib.pyplot as plt
import os

# Some important variables
COLOR = (255, 0, 0)
WHITE_COULEUR = (255, 255, 255)
WIDTH_PADDLE = 10
HEIGHT_PADDLE = 100
SPEED_PADDLE = 10
BALL_RADUIS = 10
RADUIS = 10

SCORE_MAX = 6
# Screen variables
WIDHT = 840
HEIGHT = 600

# SIMPLE AI speed
SIMPLE_AI_SPEED = 4

# FPS for Frequency per second - It's so important to accelerate the speed of the game regarding the number or trainning iteration we want to have
FPS = 520
TRANNING = True

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
        self.velocity = [np.random.uniform(2, 5), np.random.uniform(-4, 5)]

        pygame.draw.circle(self.image, color, (self.width // 2, self.height // 2), self.raduis)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]

    def ball_bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = np.random.uniform(-4, 5)

class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height, name, alpha=0.4, gamma=0.7, epsilon_decay=0.00001, epsilon_min=0.01, epsilon=1):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE_COULEUR)
        self.image.set_colorkey(WHITE_COULEUR)
        self.width = width
        self.height = height

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = {}
        self.rewards, self.episodes, self.mean = [], [], []
        self.name = name
        
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

    def simple_ai(self, ball_position_y, pixels):
        if ball_position_y + RADUIS > self.rect.y + HEIGHT_PADDLE / 2:
            self.rect.y += pixels
        if ball_position_y + RADUIS < self.rect.y + HEIGHT_PADDLE/ 2:
            self.rect.y -= pixels

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y  > (HEIGHT - self.height):
            self.rect.y = (HEIGHT - self.height)

    def epsilon_greddy(self):
        self.epsilon = max(self.epsilon_min, self.epsilon*(1 - self.epsilon_decay))

    def get_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(3)

        self.epsilon_greddy()

        if np.random.uniform() < self.epsilon:
            action = np.random.choice(3)
        else:
            action = np.argmax(self.q_table[state])

        return action
    

    """
    Update the q_table based on the actual state, the next state, the action taken by the agent and the reward
    If the next state is not in the q_table, we can add it if not we can just add considering the state and the action
    MORE DETAILS IN THE REPORT
    """
    def update_q_table(self, state, action, reward, next_state):
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(3)

        td_target = reward + self.gamma * np.max(self.q_table[next_state])
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

    def save_model(self, episode):
        folder_models = "models"
        if not os.path.exists(folder_models):
            os.makedirs(folder_models)
        path_file = os.path.join(folder_models, f'player_{self.name}_{episode}_qtable.pkl')
        with open(path_file, 'wb') as file:
            pickle.dump(self.q_table, file)

    def trace_model(self, reward, episode):
        self.rewards.append(reward)
        self.episodes.append(episode)
        self.mean.append(sum(self.rewards) / len(self.rewards))
        plt.plot(self.episodes, self.mean, 'r')
        plt.plot(self.episodes, self.rewards, 'b')
        plt.xlabel("Reward", fontsize=18)
        plt.ylabel("Episodes", fontsize=18)

        try:
            plt.savefig(f"player_{self.name}_evolution.png")
        except OSError as e:
            print(f"Error while save the file : {e}")

class Game:
    def __init__(self, player_a, player_b):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDHT, HEIGHT))
        pygame.display.set_caption("Ping Pong Game Tranning AI")

        self.paddle_a = player_a
        self.paddle_a.rect.x = 0
        self.paddle_a.rect.y = (HEIGHT - HEIGHT_PADDLE) // 2

        self.paddle_b = player_b
        self.paddle_b.rect.x = WIDHT - WIDTH_PADDLE
        self.paddle_b.rect.y = (HEIGHT - HEIGHT_PADDLE) // 2

        self.ball = Ball(COLOR, 2 * RADUIS, 2 * RADUIS, RADUIS)
        self.ball.rect.centerx = WIDHT // 2
        self.ball.rect.centery = HEIGHT // 2

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.paddle_a, self.paddle_b, self.ball)

        self.end = False
        self.clock = pygame.time.Clock()
        self.score_a, self.score_b = 0, 0
        self.reward = 0

    def get_reward(self):
        reward_max = HEIGHT_PADDLE // 2
        reward_min = -reward_max

        distance_y = abs(self.paddle_a.rect.centery - self.ball.rect.centery)
        reward =- (distance_y / HEIGHT) * reward_max
        if distance_y < HEIGHT_PADDLE // 2:
            reward += reward_max
        return max(reward_min, reward)

    def define_state_distilled(self):
        if (self.paddle_a.rect.centery - RADUIS <= self.ball.rect.centery <= self.paddle_a.rect.y + RADUIS):
            state_distilled = 0
        elif self.ball.rect.centery < self.paddle_a.rect.centery:
            state_distilled = 1
        else:
            state_distilled = 2

        return state_distilled

    def play(self):
        action_a = 0
        
        while not self.end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.end = True

            self.paddle_b.simple_ai(self.ball.rect.y, SIMPLE_AI_SPEED)

            state_distilled = self.define_state_distilled()

            # For having the state of the game, we have to combine the distilled state and also the agent action
            self.state = (
                state_distilled, 
                action_a
            )

            reward_a = 0
            action_a = self.paddle_a.get_action(self.state)

            if action_a == 1:
                self.paddle_a.move_up(SPEED_PADDLE)
            elif action_a == 2:
                self.paddle_a.move_down(SPEED_PADDLE)

            self.ball.update()

            reward_a = self.get_reward()

            if pygame.sprite.spritecollide(self.ball, [self.paddle_a], False):
                self.ball.ball_bounce()
            if pygame.sprite.spritecollide(self.ball, [self.paddle_b], False):
                self.ball.ball_bounce()

            if self.ball.rect.x > WIDHT:
                (self.ball.rect.x, self.ball.rect.y) = (WIDHT // 2, HEIGHT // 2)
                self.ball.velocity[0] *= -1
                self.score_a += 1
            elif self.ball.rect.x < 0:
                (self.ball.rect.x, self.ball.rect.y) = (WIDHT // 2, HEIGHT // 2)
                self.ball.velocity[0] *= -1
                self.score_b += 1

            if self.ball.rect.y > HEIGHT - 2*RADUIS:
                self.ball.velocity[1] *= -1
            if self.ball.rect.y < 0:
                self.ball.velocity[1] *= -1

            state_distilled = self.define_state_distilled()

            next_state = (
                state_distilled, 
                action_a
            )

            # Updating the q table after collect data
            self.paddle_a.update_q_table(self.state, action_a, reward_a, next_state)

            self.screen.fill(WHITE_COULEUR)
            pygame.draw.line(self.screen, COLOR, [WIDHT // 2, 0], [WIDHT // 2, HEIGHT], 5)
            self.all_sprites.draw(self.screen)

            font = pygame.font.Font(None, 74)
            text = font.render(str(self.score_a), 1, COLOR)
            self.screen.blit(text, (WIDHT // 4, 10))
            text = font.render(str(self.score_b), 1, COLOR)
            self.screen.blit(text, (3 * WIDHT // 4, 10))

            self.all_sprites.update()

            pygame.display.flip()
            self.clock.tick(FPS)

            self.reward += reward_a

            if self.score_a == SCORE_MAX or self.score_b == SCORE_MAX:
                self.end = True
                pygame.quit()

if __name__ == "__main__":
    player_b = Paddle(COLOR, WIDTH_PADDLE, HEIGHT_PADDLE, "B")
    player_a = Paddle(COLOR, WIDTH_PADDLE, HEIGHT_PADDLE, "A")

    for i in range(501):
        game = Game(player_a, player_b)
        game.play()
        if (i) % 10 == 0:
            player_a.save_model(i)
        player_a.trace_model(game.reward, i)
        print(f"Partie {i} : Epsilon A : {player_a.epsilon}\nScore : {game.score_a} : {game.score_b} Score B\nReward : {game.reward}\n\n")