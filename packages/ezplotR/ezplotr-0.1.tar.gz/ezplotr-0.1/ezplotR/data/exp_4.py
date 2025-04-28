#4
import numpy as np
import matplotlib.pyplot as plt

n_arms = 10
n_steps = 10000
n_runs = 2000
epsilon = 0.1
alpha = 0.1
sigma = 0.01

# Function to run the experiment
def bandit_experiment(sample_average=True):
    avg_rewards = np.zeros(n_steps)
    optimal_action_counts = np.zeros(n_steps)

    for run in range(n_runs):
        q_true = np.zeros(n_arms)  # Start with equal values
        q_est = np.zeros(n_arms)  # Estimated values
        action_counts = np.zeros(n_arms)  # Action counts (for sample-average method)
        optimal_action = np.argmax(q_true)

        for t in range(n_steps):
            if np.random.rand() < epsilon:
                action = np.random.choice(n_arms)
            else:
                action = np.argmax(q_est)

            reward = np.random.randn() + q_true[action]  # Reward with noise
            avg_rewards[t] += reward

            if action == optimal_action:
                optimal_action_counts[t] += 1

            if sample_average:
                action_counts[action] += 1
                q_est[action] += (reward - q_est[action]) / action_counts[action]
            else:
                q_est[action] += alpha * (reward - q_est[action])

            q_true += np.random.normal(0, sigma, n_arms)  # Update true values
            optimal_action = np.argmax(q_true)

    return avg_rewards / n_runs, optimal_action_counts / n_runs

rewards_sample_avg, opt_sample_avg = bandit_experiment(sample_average=True)
rewards_const_step, opt_const_step = bandit_experiment(sample_average=False)

fig, axes = plt.subplots(2, 1, figsize=(10, 10))

axes[0].plot(rewards_sample_avg, label="Sample Average", color='red')
axes[0].plot(rewards_const_step, label="Constant Step-size (α=0.1)", color='blue')
axes[0].set_ylabel("Average Reward")
axes[0].set_xlabel("Steps")
axes[0].legend()

axes[1].plot(opt_sample_avg * 100, label="Sample Average", color='red')
axes[1].plot(opt_const_step * 100, label="Constant Step-size (α=0.1)", color='blue')
axes[1].set_ylabel("% Optimal Action")
axes[1].set_xlabel("Steps")
axes[1].legend()

plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()
