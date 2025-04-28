#10

import numpy as np
import matplotlib.pyplot as plt

# Function to perform Monte Carlo simulation for estimating π
def estimate_pi(num_samples):
    # Generate random x and y coordinates between 0 and 1
    x = np.random.uniform(0, 1, num_samples)
    y = np.random.uniform(0, 1, num_samples)

    # Check if points lie inside the quarter circle (x^2 + y^2 <= 1)
    inside_circle = (x**2 + y**2) <= 1

    # Calculate the ratio of points inside the quarter circle
    pi_estimate = 4 * np.sum(inside_circle) / num_samples

    return pi_estimate, x, y, inside_circle

num_samples = 10000
np.random.seed(42)  # For reproducibility

# Run the simulation
pi_approx, x, y, inside = estimate_pi(num_samples)

print(f"Estimated value of π with {num_samples} samples: {pi_approx}")
print(f"Actual value of π: {np.pi}")
print(f"Absolute error: {abs(pi_approx - np.pi)}")

plt.figure(figsize=(6, 6))
plt.scatter(x[inside], y[inside], color='blue', s=1, label='Inside Quarter Circle')
plt.scatter(x[~inside], y[~inside], color='red', s=1, label='Outside')
plt.title(f'Monte Carlo Estimation of π\nEstimate = {pi_approx:.5f}')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.axis('equal')
plt.show()

# Analyze convergence with increasing sample sizes
sample_sizes = [100, 500, 1000, 5000, 10000, 50000]
pi_estimates = []

for n in sample_sizes:
    pi_est, _, _, _ = estimate_pi(n)
    pi_estimates.append(pi_est)

# Plot convergence
plt.plot(sample_sizes, pi_estimates, 'bo-', label='Estimated π')
plt.axhline(y=np.pi, color='r', linestyle='--', label='Actual π')
plt.xscale('log')
plt.xlabel('Number of Samples (log scale)')
plt.ylabel('Estimated Value of π')
plt.title('Convergence of Monte Carlo Estimation')
plt.legend()
plt.grid(True)
plt.show()