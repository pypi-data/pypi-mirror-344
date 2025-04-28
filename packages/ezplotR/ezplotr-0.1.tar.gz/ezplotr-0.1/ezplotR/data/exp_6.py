#6
import numpy as np

gamma = 1.0
threshold = 1e-6
actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
policy = np.ones((4, 4, 4)) / 4
V = np.zeros((4, 4))

def is_terminal(state):
    return state == (0, 0) or state == (3, 3)

def step(state, action):
    x, y = state
    dx, dy = actions[action]
    nx, ny = max(0, min(x + dx, 3)), max(0, min(y + dy, 3))
    return (nx, ny), -1

def evaluate_policy():
    while True:
        delta = 0
        for i in range(4):
            for j in range(4):
                if is_terminal((i, j)):
                    continue
                v = V[i, j]
                V[i, j] = sum(policy[i, j, a] * (r + gamma * V[s[0], s[1]])
                               for a in range(4)
                               for s, r in [step((i, j), a)])
                delta = max(delta, abs(v - V[i, j]))
        if delta < threshold:
            break
def improve_policy():
    stable = True
    for i in range(4):
        for j in range(4):
            if is_terminal((i, j)):
                continue
            old_action = np.argmax(policy[i, j])
            q_values = [sum(r + gamma * V[s[0], s[1]] for s, r in [step((i, j), a)]) for a in range(4)]
            best_action = np.argmax(q_values)
            policy[i, j] = np.eye(4)[best_action]
            if old_action != best_action:
                stable = False
    return stable

while True:
    evaluate_policy()
    if improve_policy():
        break

print("Final Value Function:")
print(V)
print("\nOptimal Policy:")
policy_symbols = ['↑', '↓', '←', '→']
for i in range(4):
    print([policy_symbols[np.argmax(policy[i, j])] if not is_terminal((i, j)) else ' ' for j in range(4)])
