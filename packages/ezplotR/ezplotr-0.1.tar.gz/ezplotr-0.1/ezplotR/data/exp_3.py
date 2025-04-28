#3
import numpy as np
import matplotlib.pyplot as plt
import random

n_bandit = 2000  # number of bandit problems
k = 10  # number of arms in each bandit problem
n_pulls = 1000  # number of times to pull each arm

# Generate the true means q*(a) for each arm for all bandits
q_true = np.random.normal(0, 1, (n_bandit, k))
true_opt_arms = np.argmax(q_true, 1)  # the true optimal arms in each bandit

epsilon = [0, 0.01, 0.1, 0.2, 1]  # epsilon in epsilon-greedy method
col = ['r', 'g', 'k', 'b', 'y']

# Creating two plots
fig1 = plt.figure().add_subplot(111)
fig2 = plt.figure().add_subplot(111)

for eps in range(len(epsilon)):
    print('Current epsilon :', epsilon[eps])

    Q = np.zeros((n_bandit, k))  # reward estimates
    N = np.ones((n_bandit, k))  # number of times each arm was pulled
    Qi = np.random.normal(q_true, 1)  # initial pulling of all arms

    R_eps = []
    R_eps.append(0)
    R_eps.append(np.mean(Qi))
    R_eps_opt = []

    for pull in range(2, n_pulls + 1):
        R_pull = []  # all rewards in this pull/time-step
        opt_arm_pull = 0  # number of pulls of the best arm in this time step

        for i in range(n_bandit):
            # Choose arm based on epsilon-greedy method
            if random.random() < epsilon[eps]:
                j = np.random.randint(k)  # explore
            else:
                j = np.argmax(Q[i])  # exploit

            if j == true_opt_arms[i]:  # Calculate percentage of optimal actions
                opt_arm_pull += 1

            # Generate a reward from the selected arm's true mean
            temp_R = np.random.normal(q_true[i][j], 1)
            R_pull.append(temp_R)

            # Update counts and reward estimates
            N[i][j] += 1
            Q[i][j] += (temp_R - Q[i][j]) / N[i][j]

        avg_R_pull = np.mean(R_pull)
        R_eps.append(avg_R_pull)
        R_eps_opt.append(float(opt_arm_pull) * 100 / n_bandit)

    # Plotting results
    fig1.plot(range(0, n_pulls + 1), R_eps, col[eps])
    fig2.plot(range(2, n_pulls + 1), R_eps_opt, col[eps])

# Set up plot titles and labels without LaTeX formatting
fig1.title.set_text('Epsilon-greedy: Average Reward Vs Steps for 10 arms')
fig1.set_ylabel('Average Reward')
fig1.set_xlabel('Steps')
fig1.legend([f"epsilon={eps}" for eps in epsilon], loc='best')

fig2.title.set_text('Epsilon-greedy: % Optimal Action Vs Steps for 10 arms')
fig2.set_ylabel('% Optimal Action')
fig2.set_xlabel('Steps')
fig2.set_ylim(0, 100)
fig2.legend([f"epsilon={eps}" for eps in epsilon], loc='best')

# Show the plots
plt.show()
