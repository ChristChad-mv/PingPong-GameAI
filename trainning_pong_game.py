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

SCORE_MAX = 5

# Screen variables
WIDHT = 840
HEIGHT = 600

# SIMPLE AI speed
SIMPLE_AI_SPEED = 3

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

    def __init__(self, color, width, height, name, alpha=0.4, gamma=0.7, epsilon_decay=0.00001, epsilon_min=0.01, epsilon=1):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE_COULEUR)
        self.image.set_colorkey(WHITE_COULEUR)
        self.width = width
        self.height = height

        self.alpha = alpha
        self.gamma = gamma
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
        if ball_position_y + BALL_RADUIS > self.rect.y + self.height / 2:
            self.rect.y += pixels
        if ball_position_y + BALL_RADUIS < self.rect.y + self.height / 2:
            self.rect.y -= pixels

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y  > (HEIGHT - self.height):
            self.rect.y = (HEIGHT - self.height)

    def epsilon_greddy(self):
        self.epsilon = max(self.epsilon_min, self.epsilon* (1 - self.epsilon_decay))

    def get_actions(self, state):
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