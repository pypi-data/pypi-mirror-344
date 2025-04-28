#7
import numpy as np

grid_size = 4
actions = ['U', 'D', 'L', 'R']
gamma = 0.9
theta = 1e-4  # Convergence threshold
reward = -1

action_effects = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

V = np.zeros((grid_size, grid_size))

terminal_state = (grid_size - 1, grid_size - 1)

# Value Iteration Algorithm
while True:
    delta = 0
    new_V = np.copy(V)

    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) == terminal_state:
                continue

            max_value = float('-inf')
            for action in actions:
                ni, nj = i + action_effects[action][0], j + action_effects[action][1]
                if 0 <= ni < grid_size and 0 <= nj < grid_size:
                    v = reward + gamma * V[ni, nj]
                else:
                    v = reward + gamma * V[i, j]

                max_value = max(max_value, v)

            new_V[i, j] = max_value
            delta = max(delta, abs(V[i, j] - new_V[i, j]))

    V = new_V

    if delta < theta:
        break

policy = np.full((grid_size, grid_size), ' ', dtype=str)

for i in range(grid_size):
    for j in range(grid_size):
        if (i, j) == terminal_state:
            policy[i, j] = 'G'
            continue

        best_action = None
        best_value = float('-inf')

        for action in actions:
            ni, nj = i + action_effects[action][0], j + action_effects[action][1]
            if 0 <= ni < grid_size and 0 <= nj < grid_size:
                v = reward + gamma * V[ni, nj]
            else:
                v = reward + gamma * V[i, j]

            if v > best_value:
                best_value = v
                best_action = action

        policy[i, j] = best_action


print("Optimal Value Function:")
print(np.round(V, 2))
print("\nOptimal Policy:")
for row in policy:
    print(" ".join(row))
