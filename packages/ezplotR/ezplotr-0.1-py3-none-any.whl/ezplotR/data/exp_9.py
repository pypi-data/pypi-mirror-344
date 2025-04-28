#9
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import time

class GridWorld:
    """
    Simple Grid World Environment
    """
    def __init__(self, grid_size=(4, 4), start_state=(0, 0), terminal_states=[(3, 3)], obstacles=[]):
        self.grid_size = grid_size
        self.rows, self.cols = grid_size
        self.start_state = start_state
        self.terminal_states = terminal_states
        self.obstacles = obstacles
        self.state = self.start_state

        self.actions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        self.action_list = list(self.actions.keys())

        self.step_reward = -1
        self.terminal_reward = 0

    def reset(self):
        """Resets the environment to the start state."""
        self.state = self.start_state
        return self.state

    def is_terminal(self, state):
        """Checks if a state is terminal."""
        return state in self.terminal_states

    def is_obstacle(self, state):
        """Checks if a state is an obstacle."""
        return state in self.obstacles

    def is_valid_state(self, state):
        """Checks if a state is within grid boundaries."""
        r, c = state
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_valid_actions(self, state):
        """Returns a list of actions that don't lead directly into a wall/boundary."""
        valid_actions = []
        r, c = state
        for action, (dr, dc) in self.actions.items():
            next_r, next_c = r + dr, c + dc
            if 0 <= next_r < self.rows and 0 <= next_c < self.cols:
                 valid_actions.append(action)
            else:
                 valid_actions.append(action)
        return self.action_list

    def step(self, action):
        """Takes an action and returns (next_state, reward, done)."""
        if self.is_terminal(self.state):
            return self.state, 0, True

        r, c = self.state
        dr, dc = self.actions[action]
        next_r, next_c = r + dr, c + dc

        next_state = (next_r, next_c)

        if not self.is_valid_state(next_state) or self.is_obstacle(next_state):
            next_state = self.state

        if self.is_terminal(next_state):
            reward = self.terminal_reward
            done = True
        else:
            reward = self.step_reward
            done = False

        self.state = next_state
        return next_state, reward, done

    def get_all_states(self):
        """Returns a list of all possible non-obstacle states."""
        all_states = []
        for r in range(self.rows):
            for c in range(self.cols):
                state = (r,c)
                if not self.is_obstacle(state):
                    all_states.append(state)
        return all_states

def random_policy(env, state):
    """
    Equiprobable random policy.
    Returns a randomly chosen valid action.
    """
    if env.is_terminal(state):
        return None

    valid_actions = env.action_list
    return random.choice(valid_actions)

def td0_policy_evaluation(env, policy_func, gamma=0.9, alpha=0.1, num_episodes=1000):
    """
    Performs TD(0) policy evaluation.

    Args:
        env: The GridWorld environment.
        policy_func: A function(env, state) -> action.
        gamma: Discount factor.
        alpha: Learning rate.
        num_episodes: Number of episodes to run.

    Returns:
        V: A dictionary mapping state -> value estimate.
        value_history: List of V dictionaries at different stages for convergence analysis.
    """
    all_states = env.get_all_states()
    V = defaultdict(float)

    for terminal in env.terminal_states:
        V[terminal] = 0

    value_history = []
    check_every = max(1, num_episodes // 20)

    print(f"Running TD(0) for {num_episodes} episodes...")
    start_time = time.time()

    for episode in range(num_episodes):
        state = env.reset()

        while True:
            action = policy_func(env, state)
            if action is None:
                 break
            next_state, reward, done = env.step(action)

            td_target = reward + gamma * V[next_state]
            td_error = td_target - V[state]
            V[state] = V[state] + alpha * td_error
            state = next_state
            if done:
                break

        if (episode + 1) % check_every == 0 or episode == num_episodes - 1:
            value_history.append(V.copy())

    end_time = time.time()
    print(f"TD(0) finished in {end_time - start_time:.2f} seconds.")

    return V, value_history

def plot_value_function(env, V, title="Value Function"):
    """Plots the value function as a heatmap."""
    value_grid = np.full(env.grid_size, np.nan)
    for r in range(env.rows):
        for c in range(env.cols):
            state = (r, c)
            if env.is_obstacle(state):
                continue
            value_grid[r, c] = V.get(state, 0)

    plt.figure(figsize=(env.cols + 1, env.rows + 1))
    im = plt.imshow(value_grid, cmap='viridis', interpolation='nearest', origin='upper')

    for r in range(env.rows):
        for c in range(env.cols):
            state = (r, c)
            if env.is_obstacle(state):
                plt.text(c, r, 'X', ha='center', va='center', color='red', fontsize=12)
            elif env.is_terminal(state):
                 plt.text(c, r, f"G\n{value_grid[r, c]:.1f}", ha='center', va='center', color='white', fontsize=10)
            else:
                plt.text(c, r, f"({r},{c})\n{value_grid[r, c]:.1f}", ha='center', va='center', color='white' if abs(value_grid[r,c]) > np.nanmax(value_grid)/2 else 'black', fontsize=9)

    start_r, start_c = env.start_state
    plt.text(start_c, start_r, 'S', ha='center', va='center', color='cyan', fontsize=12, weight='bold')


    plt.colorbar(im, label='State Value')
    plt.title(title)
    plt.xticks(np.arange(env.cols))
    plt.yticks(np.arange(env.rows))
    plt.grid(which='major', color='black', linestyle='-', linewidth=1)
    plt.show()

def plot_convergence(value_history, state_to_track, num_episodes):
    """Plots the convergence of the value estimate for a specific state."""
    values_over_time = [history[state_to_track] for history in value_history if state_to_track in history]
    episodes = np.linspace(0, len(value_history) * (num_episodes // len(value_history)), len(values_over_time))

    if not values_over_time:
        print(f"Warning: State {state_to_track} not found in history.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(episodes, values_over_time)
    plt.xlabel("Episodes")
    plt.ylabel(f"Value Estimate V{state_to_track}")
    plt.title(f"TD(0) Convergence for State {state_to_track}")
    plt.grid(True)
    plt.show()

GRID_SIZE = (4, 4)
START_STATE = (0, 0)
TERMINAL_STATES = [(3, 3)]
OBSTACLES = [(1, 1), (1, 2), (2, 2)]

GAMMA = 0.99
ALPHA = 0.1
NUM_EPISODES = 5000

env = GridWorld(grid_size=GRID_SIZE, start_state=START_STATE, terminal_states=TERMINAL_STATES, obstacles=OBSTACLES)

final_V, history_V = td0_policy_evaluation(env, random_policy, gamma=GAMMA, alpha=ALPHA, num_episodes=NUM_EPISODES)

print("\n--- Final Value Function ---")
plot_value_function(env, final_V, f"TD(0) Value Function Estimate (α={ALPHA}, γ={GAMMA}, episodes={NUM_EPISODES})")

print("\n--- Convergence Analysis ---")
state_to_track = (2, 1)
if state_to_track not in env.obstacles and not env.is_terminal(state_to_track):
    plot_convergence(history_V, state_to_track, NUM_EPISODES)
else:
    print(f"Cannot track state {state_to_track} as it's an obstacle or terminal.")

plot_convergence(history_V, env.start_state, NUM_EPISODES)