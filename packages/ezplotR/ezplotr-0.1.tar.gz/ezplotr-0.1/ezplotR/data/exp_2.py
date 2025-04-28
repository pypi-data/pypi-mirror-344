#EXP 1 2

import numpy as np
import random
import matplotlib.pyplot as plt

# Simple 4x4 GridWorld
class GridWorld:
    def __init__(self):
        self.size = 4
        self.state = (0, 0)
        self.terminal = (3, 3)

    def reset(self):
        self.state = (0, 0)
        return self.state

    def step(self, action):
        x, y = self.state
        if action == 0 and x > 0: x -= 1  # up
        if action == 1 and x < self.size-1: x += 1  # down
        if action == 2 and y > 0: y -= 1  # left
        if action == 3 and y < self.size-1: y += 1  # right
        self.state = (x, y)
        reward = 1 if self.state == self.terminal else -0.01
        done = self.state == self.terminal
        return self.state, reward, done

# Parameters
episodes = 500
alpha = 0.1
gamma = 0.99
epsilon = 0.1
actions = [0, 1, 2, 3]  # up, down, left, right

# # Q-Learning
def q_learning(env):
    Q = np.zeros((env.size, env.size, len(actions)))
    rewards = []
    for ep in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        while not done:
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                action = np.argmax(Q[state[0], state[1]])
            next_state, reward, done = env.step(action)
            best_next = np.max(Q[next_state[0], next_state[1]])
            Q[state[0], state[1], action] += alpha * (reward + gamma * best_next - Q[state[0], state[1], action])
            state = next_state
            total_reward += reward
        rewards.append(total_reward)
    return Q, rewards

# SARSA
def sarsa(env):
    Q = np.zeros((env.size, env.size, len(actions)))
    rewards = []
    for ep in range(episodes):
        state = env.reset()
        if random.random() < epsilon:
            action = random.choice(actions)
        else:
            action = np.argmax(Q[state[0], state[1]])
        done = False
        total_reward = 0
        while not done:
            next_state, reward, done = env.step(action)
            if random.random() < epsilon:
                next_action = random.choice(actions)
            else:
                next_action = np.argmax(Q[next_state[0], next_state[1]])
            Q[state[0], state[1], action] += alpha * (reward + gamma * Q[next_state[0], next_state[1], next_action] - Q[state[0], state[1], action])
            state, action = next_state, next_action
            total_reward += reward
        rewards.append(total_reward)
    return Q, rewards


# Compare
env = GridWorld()
Q_qlearning, rewards_qlearning = q_learning(env)
Q_sarsa, rewards_sarsa = sarsa(env)

print("Q-values from Q-Learning:")
print(Q_qlearning)
print("\nQ-values from SARSA:")
print(Q_sarsa)

# Plotting
plt.plot(rewards_qlearning, label="Q-Learning")
plt.plot(rewards_sarsa, label="SARSA")
plt.xlabel("Episodes")
plt.ylabel("Total Reward per Episode")
plt.title("Q-Learning vs SARSA Rewards")
plt.legend()
plt.show()
