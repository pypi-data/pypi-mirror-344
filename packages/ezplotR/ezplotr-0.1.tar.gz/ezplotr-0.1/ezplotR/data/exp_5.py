#5
import numpy as np
import matplotlib.pyplot as plt

class KArmedBandit:
    def __init__(self, k=10):
        self.k = k
        self.q_true = np.random.normal(0, 1, k)  # True action values
        self.q_estimates = np.zeros(k)  # Estimated action values
        self.action_counts = np.zeros(k)  # Count of times each action is selected

    def get_reward(self, action):
        return np.random.normal(self.q_true[action], 1)  # Reward from normal distribution

    def reset(self, optimistic_init=None):
        self.q_estimates = np.zeros(self.k) if optimistic_init is None else np.full(self.k, optimistic_init)
        self.action_counts = np.zeros(self.k)

# Upper Confidence Bound Algorithm
def ucb_bandit(k=10, steps=1000, c=2):
    bandit = KArmedBandit(k)
    rewards = np.zeros(steps)
    for t in range(1, steps + 1):
        ucb_values = bandit.q_estimates + c * np.sqrt(np.log(t) / (bandit.action_counts + 1e-5))
        action = np.argmax(ucb_values)
        reward = bandit.get_reward(action)
        bandit.action_counts[action] += 1
        bandit.q_estimates[action] += (reward - bandit.q_estimates[action]) / bandit.action_counts[action]
        rewards[t - 1] = reward
    return rewards

# Optimistic Initialization Algorithm
def optimistic_bandit(k=10, steps=1000, optimistic_init=5):
    bandit = KArmedBandit(k)
    bandit.reset(optimistic_init)
    rewards = np.zeros(steps)
    for t in range(steps):
        action = np.argmax(bandit.q_estimates)
        reward = bandit.get_reward(action)
        bandit.action_counts[action] += 1
        bandit.q_estimates[action] += (reward - bandit.q_estimates[action]) / bandit.action_counts[action]
        rewards[t] = reward
    return rewards

# Running experiments and plotting results
steps = 1000
ucb_rewards = ucb_bandit(steps=steps)
optimistic_rewards = optimistic_bandit(steps=steps)

plt.plot(np.cumsum(ucb_rewards) / (np.arange(steps) + 1), label="UCB")
plt.plot(np.cumsum(optimistic_rewards) / (np.arange(steps) + 1), label="Optimistic Initialization")
plt.xlabel("Steps")
plt.ylabel("Average Reward")
plt.legend()
plt.title("UCB vs Optimistic Initialization in k-Armed Bandit")
plt.show()