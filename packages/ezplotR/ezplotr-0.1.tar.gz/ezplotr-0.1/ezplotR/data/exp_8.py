#8
import numpy as np
import matplotlib.pyplot as plt

# Define the GridWorld environment
class GridWorld:
    def __init__(self, size=5, goal=(4, 4)):
        self.size = size
        self.goal = goal
        self.state = (0, 0)
        self.actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def reset(self):
        self.state = (0, 0)
        return self.state

    def step(self, action):
        next_state = (self.state[0] + self.actions[action][0], self.state[1] + self.actions[action][1])
        if next_state[0] < 0 or next_state[0] >= self.size or next_state[1] < 0 or next_state[1] >= self.size:
            next_state = self.state  # Stay in place if out of bounds
        reward = 1 if next_state == self.goal else -0.01
        self.state = next_state
        done = self.state == self.goal
        return next_state, reward, done

# Q-Learning algorithm
def q_learning(env, episodes=500, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = np.zeros((env.size, env.size, 4))
    rewards = []
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        while not done:
            if np.random.rand() < epsilon:
                action = np.random.choice(4)
            else:
                action = np.argmax(Q[state[0], state[1]])

            next_state, reward, done = env.step(action)
            Q[state[0], state[1], action] += alpha * (reward + gamma * np.max(Q[next_state[0], next_state[1]]) - Q[state[0], state[1], action])
            state = next_state
            total_reward += reward
        rewards.append(total_reward)
        if episode == 0:
                  print(f"Q-Learning :-")
        if episode % 100 == 0:
            print(f"Episode {episode}: Total Reward = {total_reward}")
    return Q, rewards

# Double Q-Learning algorithm
def double_q_learning(env, episodes=500, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q1 = np.zeros((env.size, env.size, 4))
    Q2 = np.zeros((env.size, env.size, 4))
    rewards = []
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        while not done:
            if np.random.rand() < epsilon:
                action = np.random.choice(4)
            else:
                action = np.argmax(Q1[state[0], state[1]] + Q2[state[0], state[1]])

            next_state, reward, done = env.step(action)
            if np.random.rand() < 0.5:
                a_next = np.argmax(Q1[next_state[0], next_state[1]])
                Q1[state[0], state[1], action] += alpha * (reward + gamma * Q2[next_state[0], next_state[1], a_next] - Q1[state[0], state[1], action])
            else:
                a_next = np.argmax(Q2[next_state[0], next_state[1]])
                Q2[state[0], state[1], action] += alpha * (reward + gamma * Q1[next_state[0], next_state[1], a_next] - Q2[state[0], state[1], action])

            state = next_state
            total_reward += reward
        rewards.append(total_reward)
        if episode == 0:
                  print(f"Double Q-Learning :-")
        if episode % 100 == 0:
            print(f"Episode {episode}: Total Reward = {total_reward}")
    return Q1 + Q2, rewards

# Run experiments
env = GridWorld()
q_table, q_rewards = q_learning(env)
dq_table, dq_rewards = double_q_learning(env)

# Plot comparison
plt.plot(q_rewards, label='Q-Learning')
plt.plot(dq_rewards, label='Double Q-Learning')
plt.xlabel('Episodes')
plt.ylabel('Total Reward')
plt.legend()
plt.title('Q-Learning vs. Double Q-Learning Performance')
plt.show()
