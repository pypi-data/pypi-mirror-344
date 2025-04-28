def acf(selection):
    switcher = {
        0: '''
1 Implement a simple grid-world environment and train an agent using basic Q learning using Python.
2 Implement State Action Reward State Action (SARSA) algorithm using Python and compare it with Q Learning.
3 Implement a multi-armed bandit problem and understand Epsilon Value.
4 Evaluate Sample-Average Methods in Non-stationary Bandit Problems.
5 Experiment with Upper Confidence Bound and Optimistic Initialization strategy and analyze its impact on the learning performance of an agent.
6 Implement a basic grid-world environment as an MDP and apply policy evaluation and policy iteration on it.
7 Apply a value iteration algorithm to find optimal policies for the grid-world environment.
8 Implement and analyze the Double Q-Learning algorithm to address maximization bias in Q-Learning.
9 Implement and analyze the Temporal Difference (TD) Learning algorithm (TD(0)) for policy evaluation in a grid-world environment.
10 Implement and analyze Monte Carlo methods using Python Programming.

        ''',
        1: '''import numpy as np
import random

# Define the gridworld environment
class GridWorld:
    def __init__(self):
        self.grid = np.array([
            [0, 0, 0, 1],  # Goal at (0, 3)
            [0, -1, 0, 0],  # Wall with reward -1
            [-1, -1, -1, 0],
            [0, 0, 0, 0]  # Start at (3, 0)
        ])
        self.start_state = (3, 0)
        self.state = self.start_state

    def reset(self):
        self.state = self.start_state
        return self.state

    def is_terminal(self, state):
        return self.grid[state] == 1 or self.grid[state] == -1

    def get_next_state(self, state, action):
        next_state = list(state)
        if action == 0:  # Move up
            next_state[0] = max(0, state[0] - 1)
        elif action == 1:  # Move right
            next_state[1] = min(3, state[1] + 1)
        elif action == 2:  # Move down
            next_state[0] = min(3, state[0] + 1)
        elif action == 3:  # Move left
            next_state[1] = max(0, state[1] - 1)
        return tuple(next_state)

    def step(self, action):
        next_state = self.get_next_state(self.state, action)
        reward = self.grid[next_state]
        self.state = next_state
        done = self.is_terminal(next_state)
        return next_state, reward, done


# Q-Learning Agent
class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.q_table = np.zeros((4, 4, 4))  # Q-values for each state-action pair
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, 3)  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def update_q_value(self, state, action, reward, next_state):
        max_future_q = np.max(self.q_table[next_state])  # Best Q-value for next state
        current_q = self.q_table[state][action]
        # Q-learning formula
        self.q_table[state][action] = current_q + self.learning_rate * (
            reward + self.discount_factor * max_future_q - current_q
        )

    def get_policy(self):
        # Get the optimal policy (direction) for each state
        policy = np.zeros((4, 4), dtype=str)
        for i in range(4):
            for j in range(4):
                if env.grid[i, j] == 1:
                    policy[i, j] = 'G'  # Goal
                elif env.grid[i, j] == -1:
                    policy[i, j] = 'W'  # Wall
                else:
                    best_action = np.argmax(self.q_table[i, j])
                    if best_action == 0:
                        policy[i, j] = '↑'  # Up
                    elif best_action == 1:
                        policy[i, j] = '→'  # Right
                    elif best_action == 2:
                        policy[i, j] = '↓'  # Down
                    elif best_action == 3:
                        policy[i, j] = '←'  # Left
        return policy


# Function to print Q-table and policy
def print_results(agent, alpha):
    print(f"\nResults for alpha (learning rate) = {alpha}:")
    print("\nQ-table:")
    for i in range(4):
        for j in range(4):
            print(f"State ({i}, {j}): {agent.q_table[i, j]}")
    print("\nPolicy (Direction Table):")
    policy = agent.get_policy()
    for row in policy:
        print(" ".join(row))


# Training the Agent with different alpha values
alphas = [0.1, 0.5, 0.9]  # Different learning rates to test
episodes = 1000  # Number of training episodes

for alpha in alphas:
    env = GridWorld()
    agent = QLearningAgent(learning_rate=alpha)

    for episode in range(episodes):
        state = env.reset()  # Reset the environment at the start of each episode
        done = False

        while not done:
            action = agent.choose_action(state)  # Choose an action
            next_state, reward, done = env.step(action)  # Take the action and observe next state, reward
            agent.update_q_value(state, action, reward, next_state)  # Update Q-values
            state = next_state  # Move to the next state

    # Print Q-table and policy for the current alpha
    print_results(agent, alpha)
            ''',
        2: '''
            import numpy as np
import random

# Define the 6x6 gridworld environment with multiple rewards
class GridWorld:
    def __init__(self):
        # 6x6 grid with multiple rewards and holes
        self.grid = np.array([
            [0, 0, 0, 0, 0, 10],  # High reward at (0, 5)
            [0, -1, 0, 0, -1, 0],  # Holes at (1, 1) and (1, 4)
            [0, 0, 0, 0, 0, 0],
            [0, 0, -1, 0, 0, 5],  # Hole at (3, 2), reward at (3, 5)
            [0, 0, 0, 0, -1, 0],  # Hole at (4, 4)
            [1, 0, 0, 0, 0, 0]  # Start at (5, 0), small reward at (5, 0)
        ])
        self.start_state = (5, 0)
        self.state = self.start_state

    def reset(self):
        self.state = self.start_state
        return self.state

    def is_terminal(self, state):
        # Terminal states are holes or any state with a reward
        return self.grid[state] == -1 or self.grid[state] > 0

    def get_next_state(self, state, action):
        next_state = list(state)
        if action == 0:  # Move up
            next_state[0] = max(0, state[0] - 1)
        elif action == 1:  # Move right
            next_state[1] = min(5, state[1] + 1)
        elif action == 2:  # Move down
            next_state[0] = min(5, state[0] + 1)
        elif action == 3:  # Move left
            next_state[1] = max(0, state[1] - 1)
        return tuple(next_state)

    def step(self, action):
        next_state = self.get_next_state(self.state, action)
        reward = self.grid[next_state]
        self.state = next_state
        done = self.is_terminal(next_state)
        return next_state, reward, done


# Q-Learning Agent
class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.q_table = np.zeros((6, 6, 4))  # Q-values for each state-action pair
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, 3)  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def update_q_value(self, state, action, reward, next_state, next_action=None):
        max_future_q = np.max(self.q_table[next_state])  # Best Q-value for next state
        current_q = self.q_table[state][action]
        # Q-learning formula
        self.q_table[state][action] = current_q + self.learning_rate * (
            reward + self.discount_factor * max_future_q - current_q
        )

    def get_policy(self):
        # Get the optimal policy (direction) for each state
        policy = np.zeros((6, 6), dtype=str)
        for i in range(6):
            for j in range(6):
                if env.grid[i, j] == -1:
                    policy[i, j] = 'H'  # Hole
                elif env.grid[i, j] > 0:
                    policy[i, j] = 'R'  # Reward
                else:
                    best_action = np.argmax(self.q_table[i, j])
                    if best_action == 0:
                        policy[i, j] = '↑'  # Up
                    elif best_action == 1:
                        policy[i, j] = '→'  # Right
                    elif best_action == 2:
                        policy[i, j] = '↓'  # Down
                    elif best_action == 3:
                        policy[i, j] = '←'  # Left
        return policy


# SARSA Agent
class SarsaAgent(QLearningAgent):
    def update_q_value(self, state, action, reward, next_state, next_action):
        # SARSA formula
        next_q = self.q_table[next_state][next_action]
        current_q = self.q_table[state][action]
        self.q_table[state][action] = current_q + self.learning_rate * (
            reward + self.discount_factor * next_q - current_q
        )


# Function to print Q-table and policy
def print_results(agent, algorithm, alpha, gamma, total_reward):
    print(f"\nResults for {algorithm} (alpha = {alpha}, gamma = {gamma}):")
    print(f"Total Reward Accumulated: {total_reward}")
    print("\nPolicy (Direction Table):")
    policy = agent.get_policy()
    for row in policy:
        print(" ".join(row))


# Training the Agents with different alpha and gamma values
alphas = [0.1, 0.5, 0.9]  # Different learning rates to test
gammas = [0.5, 0.9, 0.99]  # Different discount factors to test
episodes = 1000  # Number of training episodes

# Store results for each combination
results = []

for alpha in alphas:
    for gamma in gammas:
        # Train Q-Learning Agent
        env = GridWorld()
        q_agent = QLearningAgent(learning_rate=alpha, discount_factor=gamma)
        q_total_reward = 0

        for episode in range(episodes):
            state = env.reset()
            done = False
            while not done:
                action = q_agent.choose_action(state)
                next_state, reward, done = env.step(action)
                q_agent.update_q_value(state, action, reward, next_state)
                state = next_state
                q_total_reward += reward

        # Train SARSA Agent
        env = GridWorld()
        sarsa_agent = SarsaAgent(learning_rate=alpha, discount_factor=gamma)
        sarsa_total_reward = 0

        for episode in range(episodes):
            state = env.reset()
            done = False
            action = sarsa_agent.choose_action(state)
            while not done:
                next_state, reward, done = env.step(action)
                next_action = sarsa_agent.choose_action(next_state)
                sarsa_agent.update_q_value(state, action, reward, next_state, next_action)
                state = next_state
                action = next_action
                sarsa_total_reward += reward

        # Store results for this combination
        results.append({
            "alpha": alpha,
            "gamma": gamma,
            "q_total_reward": q_total_reward,
            "sarsa_total_reward": sarsa_total_reward,
            "q_policy": q_agent.get_policy(),
            "sarsa_policy": sarsa_agent.get_policy()
        })

        # Print results for this combination
        print_results(q_agent, "Q-Learning", alpha, gamma, q_total_reward)
        print_results(sarsa_agent, "SARSA", alpha, gamma, sarsa_total_reward)

# Determine the best combination for Q-Learning and SARSA
best_q_result = max(results, key=lambda x: x["q_total_reward"])
best_sarsa_result = max(results, key=lambda x: x["sarsa_total_reward"])

print("\nBest Combination for Q-Learning:")
print(f"Alpha: {best_q_result['alpha']}, Gamma: {best_q_result['gamma']}, Total Reward: {best_q_result['q_total_reward']}")
print("\nBest Policy (Direction Table) for Q-Learning:")
for row in best_q_result["q_policy"]:
    print(" ".join(row))

print("\nBest Combination for SARSA:")
print(f"Alpha: {best_sarsa_result['alpha']}, Gamma: {best_sarsa_result['gamma']}, Total Reward: {best_sarsa_result['sarsa_total_reward']}")
print("\nBest Policy (Direction Table) for SARSA:")
for row in best_sarsa_result["sarsa_policy"]:
    print(" ".join(row))
            ''',
        3: '''
        import numpy as np
        import matplotlib.pyplot as plt
        def sample_action(mean, spread=2.0):
            return np.random.uniform(mean - spread, mean + spread)
        def executor(runs=2000, time_steps=300, epsilon=0.1):
            rewards_agg = []
            for i in range(runs):
                rewards_history = []

                qstar = np.array([10, 8, 5])

                qa = np.zeros(3)
                action_counts = np.zeros(3)

                for n in range(time_steps):
                    if np.random.rand() > epsilon:
                        action = np.argmax(qa)
                    else:
                        action = np.random.choice(np.arange(3))

                    reward = sample_action(qstar[action])
                    rewards_history.append(reward)

                    action_counts[action] += 1
                    qa[action] = qa[action] + 1 / action_counts[action] * (reward - qa[action])

                rewards_agg.append(rewards_history)

            stacked = np.vstack(rewards_agg)
            averaged_array = np.mean(stacked, axis=0)
            return averaged_array
    results_eps_greedy_10 = executor(epsilon=0.1)
results_eps_greedy_1 = executor(epsilon=0.01)
results_greedy = executor(epsilon=0)
# Plotting
plt.plot(results_eps_greedy_10, color="blue", label="ε = 0.1")
plt.plot(results_eps_greedy_1, color="red", label="ε = 0.01")
plt.plot(results_greedy, color="green", label="Greedy (ε = 0)")
plt.xlabel("Days")
plt.ylabel("Average Reward")
plt.title("Comparison of ε-greedy and Greedy Methods")
plt.legend()
plt.grid(True)

import numpy as np
import matplotlib.pyplot as plt

def sample_action(true_value):
    return np.random.normal(true_value, 1)

def executor(runs=2000, time_steps=300, epsilon=0.1):
    optimal_action_counts = []

    for i in range(runs):
        optimal_action_history = []

        qstar = np.array([10, 8, 5])

        optimal_action = np.argmax(qstar)

        qa = np.zeros(3)
        action_counts = np.zeros(3)

        for n in range(time_steps):
            if np.random.rand() > epsilon:
                action = np.argmax(qa)
            else:
                action = np.random.choice(np.arange(3))

            optimal_action_history.append(1 if action == optimal_action else 0)

            action_counts[action] += 1
            reward = sample_action(qstar[action])
            qa[action] = qa[action] + 1 / action_counts[action] * (reward - qa[action])

        optimal_action_counts.append(optimal_action_history)

    stacked_optimal = np.vstack(optimal_action_counts)
    optimal_action_percentage = np.mean(stacked_optimal, axis=0) * 100

    return optimal_action_percentage

optimal_eps_0_1 = executor(epsilon=0.1)
optimal_eps_0_01 = executor(epsilon=0.01)
optimal_greedy = executor(epsilon=0)

plt.figure(figsize=(10, 5))
plt.plot(optimal_eps_0_1, color="blue", label="ε = 0.1")
plt.plot(optimal_eps_0_01, color="red", label="ε = 0.01")
plt.plot(optimal_greedy, color="green", label="Greedy (ε = 0)")
plt.xlabel("Days")
plt.ylabel("% Optimal Action")
plt.title("Percentage of Optimal Actions vs Days")
plt.legend()
plt.grid(True)
plt.show()
            ''',
        4: '''
            import numpy as np
import matplotlib.pyplot as plt

class NonstationaryBandit:
    def __init__(self, k=10):
        self.k = k
        self.q_star = np.zeros(k)  # All actions start with the same value

    def get_reward(self, action):
        return np.random.normal(self.q_star[action], 1)

    def step(self):
        self.q_star += np.random.normal(0, 0.01, self.k)  # Random walk for nonstationary setting

class Agent:
    def __init__(self, k=10, epsilon=0.1, alpha=None):
        self.k = k
        self.epsilon = epsilon
        self.alpha = alpha  # If None, use sample-average update
        self.Q = np.zeros(k)
        self.N = np.zeros(k)  # Count of actions taken

    def select_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.k)  # Explore
        else:
            return np.argmax(self.Q)  # Exploit

    def update(self, action, reward):
        self.N[action] += 1
        if self.alpha is None:
            self.Q[action] += (1 / self.N[action]) * (reward - self.Q[action])  # Sample average
        else:
            self.Q[action] += self.alpha * (reward - self.Q[action])  # Constant step-size

def run_experiment(k=10, steps=10000, runs=100, epsilon=0.1, alpha=None):
    avg_rewards = np.zeros(steps)
    optimal_action_counts = np.zeros(steps)

    for _ in range(runs):
        bandit = NonstationaryBandit(k)
        agent = Agent(k, epsilon, alpha)

        for step in range(steps):
            action = agent.select_action()
            reward = bandit.get_reward(action)
            agent.update(action, reward)
            bandit.step()  # Update true values

            optimal_action = np.argmax(bandit.q_star)
            avg_rewards[step] += reward
            optimal_action_counts[step] += (action == optimal_action)

    avg_rewards /= runs
    optimal_action_counts = (optimal_action_counts / runs) * 100  # Convert to %
    return avg_rewards, optimal_action_counts

# Run experiments
steps = 10000
rewards_sample_avg, opt_actions_sample_avg = run_experiment(steps=steps, epsilon=0.1, alpha=None)
rewards_const_step, opt_actions_const_step = run_experiment(steps=steps, epsilon=0.1, alpha=0.1)

# Plot results
fig, axes = plt.subplots(2, 1, figsize=(10, 10))

axes[0].plot(rewards_sample_avg, label='Sample Average', color='blue')
axes[0].plot(rewards_const_step, label='Constant Step-size (α=0.1)', color='red')
axes[0].set_xlabel("Steps")
axes[0].set_ylabel("Average Reward")
axes[0].legend()
axes[0].set_title("Average Reward Over Time")

axes[1].plot(opt_actions_sample_avg, label='Sample Average', color='blue')
axes[1].plot(opt_actions_const_step, label='Constant Step-size (α=0.1)', color='red')
axes[1].set_xlabel("Steps")
axes[1].set_ylabel("% Optimal Action")
axes[1].legend()
axes[1].set_title("% Optimal Action Over Time")

plt.show()
import numpy as np
import matplotlib.pyplot as plt

class NonStationaryBandit:
    def __init__(self, k=10, epsilon=0.1, alpha=0.1, steps=10000, method='sample_average'):
        self.k = k  # Number of arms
        self.epsilon = epsilon  # Epsilon for epsilon-greedy
        self.alpha = alpha  # Step size for constant step-size method
        self.steps = steps  # Number of steps
        self.method = method  # Action-value method

        self.q_star = np.zeros(k)  # True action values
        self.q_estimates = np.zeros(k)  # Estimated action values
        self.action_counts = np.zeros(k)  # Count of actions taken (for sample-average method)
        self.rewards = []  # Store rewards over time

    def select_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.k)  # Explore
        return np.argmax(self.q_estimates)  # Exploit

    def update_q_estimates(self, action, reward):
        if self.method == 'sample_average':
            self.action_counts[action] += 1
            self.q_estimates[action] += (reward - self.q_estimates[action]) / self.action_counts[action]
        elif self.method == 'constant_step_size':
            self.q_estimates[action] += self.alpha * (reward - self.q_estimates[action])

    def run(self):
        for _ in range(self.steps):
            action = self.select_action()
            reward = np.random.normal(self.q_star[action], 1)
            self.rewards.append(reward)
            self.update_q_estimates(action, reward)
            self.q_star += np.random.normal(0, 0.01, self.k)  # Random walk for nonstationarity

# Experiment setup
def run_experiment(k=10, steps=10000, epsilon=0.1, alpha=0.1):
    sample_avg_bandit = NonStationaryBandit(k, epsilon, alpha, steps, method='sample_average')
    constant_step_bandit = NonStationaryBandit(k, epsilon, alpha, steps, method='constant_step_size')

    sample_avg_bandit.run()
    constant_step_bandit.run()

    plt.figure(figsize=(10, 5))
    plt.plot(np.cumsum(sample_avg_bandit.rewards) / np.arange(1, steps + 1),color="blue", label='Sample Average')
    plt.plot(np.cumsum(constant_step_bandit.rewards) / np.arange(1, steps + 1),color="red", label='Constant Step Size (α=0.1)')
    plt.xlabel('Steps')
    plt.ylabel('Average Reward')
    plt.legend()
    plt.title('Performance of Action-Value Methods in a Nonstationary Bandit Problem')
    plt.grid(True)
    plt.show()

# Run the experiment
run_experiment()
        ''',
        5:'''
def get_argmax(Q):
    max_value = np.max(Q)
    return np.random.choice(np.where(Q == max_value)[0])

# Simulate the bandit arm pull, return reward and whether the optimal action was taken
def bandit(q_star, action):
    reward = np.random.normal(q_star[action], 1.0)
    is_optim = int(action == np.argmax(q_star))
    return reward, is_optim

def image_from_url(url):
    return Image(url=url, width=400)

import numpy as np
import matplotlib.pyplot as plt

def run_bandit(K, q_star, rewards, optim_acts_ratio, epsilon, num_steps=1000, Q_init=0):
    Q = np.full(K, Q_init)
    N = np.zeros(K)
    ttl_optim_acts = 0

    for i in range(num_steps):
        if np.random.random() > epsilon:
            A = get_argmax(Q)
        else:
            A = np.random.randint(0, K)

        R, is_optim = bandit(q_star, A)
        N[A] += 1
        Q[A] += (R - Q[A]) / N[A]

        ttl_optim_acts += is_optim
        rewards[i] = R
        optim_acts_ratio[i] = ttl_optim_acts / (i + 1)

def run_bandit_UCB(K, q_star, rewards, optim_acts_ratio, c, num_steps=1000, Q_init=0):
    Q = np.full(K, Q_init)
    N = np.zeros(K)
    ttl_optim_acts = 0

    for i in range(num_steps):
        if 0 in N:
            A = np.random.choice(np.where(N == 0)[0])
        else:
            confidence = c * np.sqrt(np.log(i + 1) / N)
            A = np.argmax(Q + confidence)

        R, is_optim = bandit(q_star, A)
        N[A] += 1
        Q[A] += (R - Q[A]) / N[A]

        ttl_optim_acts += is_optim
        rewards[i] = R
        optim_acts_ratio[i] = ttl_optim_acts / (i + 1)

if __name__ == "__main__":
    K = 10
    num_steps = 1000
    total_rounds = 200
    q_star = np.random.normal(0, 1.0, K)

    params = {
        'greedy_0': (0.0, 0), 'greedy_10': (0.0, 10),
        'eps_0': (0.1, 0), 'eps_10': (0.1, 10),
        'ucb_0': (2, 0), 'ucb_10': (2, 10)
    }

    rewards = {}
    optim_acts_ratio = {}

    for label, (param, Q_init) in params.items():
        avg_rewards = np.zeros((total_rounds, num_steps))
        avg_optim_acts = np.zeros((total_rounds, num_steps))

        for r in range(total_rounds):
            if 'ucb' in label:
                run_bandit_UCB(K, q_star, avg_rewards[r], avg_optim_acts[r], c=param, num_steps=num_steps, Q_init=Q_init)
            else:
                run_bandit(K, q_star, avg_rewards[r], avg_optim_acts[r], epsilon=param, num_steps=num_steps, Q_init=Q_init)

        rewards[label] = avg_rewards.mean(axis=0)
        optim_acts_ratio[label] = avg_optim_acts.mean(axis=0)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    for label in ['greedy_0', 'eps_0', 'ucb_0']:
        axes[0, 0].plot(rewards[label], label=f'Avg Reward - {label}')
        axes[0, 1].plot(optim_acts_ratio[label], label=f'Optimal Action - {label}')

    axes[0, 0].set_title('Average Reward (greedy_0, eps_0, ucb_0)')
    axes[0, 0].set_xlabel('Steps')
    axes[0, 0].set_ylabel('Avg Reward')
    axes[0, 0].legend()

    axes[0, 1].set_title('Optimal Action Ratio (greedy_0, eps_0, ucb_0)')
    axes[0, 1].set_xlabel('Steps')
    axes[0, 1].set_ylabel('Optimal Action %')
    axes[0, 1].legend()

    for label in ['greedy_10', 'eps_10', 'ucb_10']:
        axes[1, 0].plot(rewards[label], label=f'Avg Reward - {label}')
        axes[1, 1].plot(optim_acts_ratio[label], label=f'Optimal Action - {label}')

    axes[1, 0].set_title('Average Reward (greedy_10, eps_10, ucb_10)')
    axes[1, 0].set_xlabel('Steps')
    axes[1, 0].set_ylabel('Avg Reward')
    axes[1, 0].legend()

    axes[1, 1].set_title('Optimal Action Ratio (greedy_10, eps_10, ucb_10)')
    axes[1, 1].set_xlabel('Steps')
    axes[1, 1].set_ylabel('Optimal Action %')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.show()
        ''',
        6:'''
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.table import Table

matplotlib.use('Agg')

WORLD_SIZE = 4
ACTIONS = [np.array([0, -1]),  # Left
           np.array([-1, 0]),  # Up
           np.array([0, 1]),   # Right
           np.array([1, 0])]   # Down
ACTION_SYMBOLS = ['←', '↑', '→', '↓']


def is_terminal(state):
    x, y = state
    return (x == 0 and y == 0) or (x == WORLD_SIZE - 1 and y == WORLD_SIZE - 1)


def step(state, action):
    if is_terminal(state):
        return state, 0

    next_state = (np.array(state) + action).tolist()
    x, y = next_state

    if x < 0 or x >= WORLD_SIZE or y < 0 or y >= WORLD_SIZE:
        next_state = state

    reward = -1
    return next_state, reward


def draw_policy(policy):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tb = Table(ax, bbox=[0, 0, 1, 1])

    nrows, ncols = policy.shape
    width, height = 1.0 / ncols, 1.0 / nrows

    # Add cells
    for (i, j), val in np.ndenumerate(policy):
        tb.add_cell(i, j, width, height, text=val, loc='center', facecolor='white')

    ax.add_table(tb)
    plt.savefig(f'policy_iteration.png')
    plt.close()


def compute_state_value_and_policy(in_place=True, discount=0.9):
    new_state_values = np.zeros((WORLD_SIZE, WORLD_SIZE))
    policy = np.full((WORLD_SIZE, WORLD_SIZE), '', dtype=object)  # Stores arrows as text
    iteration = 0

    while True:
        if in_place:
            state_values = new_state_values
        else:
            state_values = new_state_values.copy()
        old_state_values = state_values.copy()

        for i in range(WORLD_SIZE):
            for j in range(WORLD_SIZE):
                if is_terminal([i, j]):
                    policy[i, j] = '•'
                    continue

                action_values = []
                for action in ACTIONS:
                    (next_i, next_j), reward = step([i, j], action)
                    action_values.append(reward + discount * state_values[next_i, next_j])

                best_value = np.max(action_values)
                best_actions = [ACTION_SYMBOLS[idx] for idx, val in enumerate(action_values) if val == best_value]

                # Join multiple arrows if needed
                policy[i, j] = ''.join(best_actions)

                new_state_values[i, j] = best_value

        max_delta_value = abs(old_state_values - new_state_values).max()
        print(f"Iteration {iteration}:\nState Values:\n{np.round(new_state_values, 2)}\nPolicy:\n{policy}\n")

        if max_delta_value < 1e-4:
            break

        iteration += 1

    return new_state_values, policy, iteration


def figure_4_1():
    values, policy, sync_iteration = compute_state_value_and_policy(in_place=False)
    print(f"Synchronous Value Iteration completed in {sync_iteration} iterations.")

    print("\nFinal Policy:")
    print(policy)
    draw_policy(policy)


if __name__ == '__main__':
    figure_4_1()

        ''',
        7:'''
import numpy as np

# Define the grid world dimensions
grid_size = 4

gamma = 1.0  # Discount factor
theta = 1e-4  # Convergence threshold
actions = ['U', 'D', 'L', 'R']  # Up, Down, Left, Right

def step(state, action):
    """Returns the next state and reward for a given state and action."""
    i, j = state
    if action == 'U':
        next_state = (max(i - 1, 0), j)
    elif action == 'D':
        next_state = (min(i + 1, grid_size - 1), j)
    elif action == 'L':
        next_state = (i, max(j - 1, 0))
    else:  # 'R'
        next_state = (i, min(j + 1, grid_size - 1))

    reward = -1
    return next_state, reward

def value_iteration():
    """Performs value iteration on the grid world."""
    V = np.zeros((grid_size, grid_size))  # Initialize value function
    policy = np.zeros((grid_size, grid_size), dtype=str)

    iteration = 0
    while True:
        delta = 0
        new_V = V.copy()
        print(f"Iteration {iteration}:")
        print(new_V)
        iteration += 1

        for i in range(grid_size):
            for j in range(grid_size):
                if (i, j) == (0, 0) or (i, j) == (grid_size - 1, grid_size - 1):
                    continue  # Terminal states

                values = []
                for action in actions:
                    next_state, reward = step((i, j), action)
                    values.append(reward + gamma * V[next_state])

                new_V[i, j] = max(values)
                delta = max(delta, abs(V[i, j] - new_V[i, j]))

        V = new_V.copy()
        if delta < theta:
            break

    # Derive optimal policy
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) == (0, 0) or (i, j) == (grid_size - 1, grid_size - 1):
                policy[i, j] = 'T'  # Terminal state
                continue

            values = []
            action_values = {}
            for action in actions:
                next_state, reward = step((i, j), action)
                action_value = reward + gamma * V[next_state]
                values.append(action_value)
                action_values[action] = action_value

            best_action = max(action_values, key=action_values.get)
            policy[i, j] = best_action

    print("Optimal Policy:")
    print(policy)
    return V, policy

if __name__ == '__main__':
    value_iteration()

        ''',
        8:'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
%matplotlib inline
import copy

STATE_A = 0

STATE_B = 1

STATE_TERMINAL = 2

STATE_START = STATE_A

ACTION_A_RIGHT = 0
ACTION_A_LEFT = 1

EPSILON = 0.1

ALPHA = 0.1

GAMMA = 1.0

ACTIONS_B = range(0, 10)

STATE_ACTIONS = [[ACTION_A_RIGHT, ACTION_A_LEFT], ACTIONS_B]

# state action pair values, if a state is a terminal state, then the value is always 0
INITIAL_Q = [np.zeros(2), np.zeros(len(ACTIONS_B)), np.zeros(1)]

# set up destination for each state and each action
TRANSITION = [[STATE_TERMINAL, STATE_B], [STATE_TERMINAL] * len(ACTIONS_B)]

# choose an action based on epsilon greedy algorithm
def choose_action(state, q_value):
    if np.random.binomial(1, EPSILON) == 1:
        return np.random.choice(STATE_ACTIONS[state])
    else:
        values_ = q_value[state]
        return np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])

# take @action in @state, return the reward
def take_action(state, action):
    if state == STATE_A:
        return 0
    return np.random.normal(-0.1, 1)

# if there are two state action pair value array, use double Q-Learning
# otherwise use normal Q-Learning
def q_learning(q1, q2=None):
    state = STATE_START
    # track the # of action left in state A
    left_count = 0
    while state != STATE_TERMINAL:
        if q2 is None:
            action = choose_action(state, q1)
        else:
            # derive a action form Q1 and Q2
            action = choose_action(state, [item1 + item2 for item1, item2 in zip(q1, q2)])
        if state == STATE_A and action == ACTION_A_LEFT:
            left_count += 1
        reward = take_action(state, action)
        next_state = TRANSITION[state][action]
        if q2 is None:
            active_q = q1
            target = np.max(active_q[next_state])
        else:
            if np.random.binomial(1, 0.5) == 1:
                active_q = q1
                target_q = q2
            else:
                active_q = q2
                target_q = q1
            best_action = np.random.choice([action_ for action_, value_ in enumerate(active_q[next_state]) if value_ == np.max(active_q[next_state])])
            target = target_q[next_state][best_action]

        # Q-Learning update
        active_q[state][action] += ALPHA * (
            reward + GAMMA * target - active_q[state][action])
        state = next_state
    return left_count

# Figure 6.7, 1,000 runs may be enough, # of actions in state B will also affect the curves
def figure_6_7():
    # each independent run has 300 episodes
    episodes = 300
    runs = 1000
    left_counts_q = np.zeros((runs, episodes))
    left_counts_double_q = np.zeros((runs, episodes))
    for run in tqdm(range(runs)):
        q = copy.deepcopy(INITIAL_Q)
        q1 = copy.deepcopy(INITIAL_Q)
        q2 = copy.deepcopy(INITIAL_Q)
        for ep in range(0, episodes):
            left_counts_q[run, ep] = q_learning(q)
            left_counts_double_q[run, ep] = q_learning(q1, q2)
    left_counts_q = left_counts_q.mean(axis=0)
    left_counts_double_q = left_counts_double_q.mean(axis=0)

    plt.plot(left_counts_q, label='Q-Learning')
    plt.plot(left_counts_double_q, label='Double Q-Learning')
    plt.plot(np.ones(episodes) * 0.05, label='Optimal')
    plt.xlabel('episodes')
    plt.ylabel('% left actions from A')
    plt.legend()

    plt.savefig('figure_67.png')
    plt.close()

    plt.plot(1-left_counts_q, label='Q-Learning')
    plt.plot(1-left_counts_double_q, label='Double Q-Learning')
    plt.plot(np.ones(episodes) * 0.95, label='Optimal')
    plt.xlabel('episodes')
    plt.ylabel('% right actions from A')
    plt.legend()

    plt.savefig('figure_68.png')
    display_saved_images()

# Function to display saved images
def display_saved_images():
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Load and display first image
    img1 = plt.imread('figure_67.png')
    ax[0].imshow(img1)
    ax[0].axis('off')
    ax[0].set_title('Percentage of Left Actions')

    # Load and display second image
    img2 = plt.imread('figure_68.png')
    ax[1].imshow(img2)
    ax[1].axis('off')
    ax[1].set_title('Percentage of Right Actions')

if __name__ == '__main__':
    figure_6_7()
        ''',
        9: '''
            import numpy as np
import matplotlib.pyplot as plt

class GridWorld:
    def __init__(self, size=5, terminal_states=None, rewards=None):
        self.size = size
        self.terminal_states = terminal_states if terminal_states else []
        self.rewards = rewards if rewards else {}
        self.actions = ['up', 'down', 'left', 'right']

    def get_next_state(self, state, action):
        x, y = state
        if state in self.terminal_states:
            return state

        if action == 'up':
            x = max(0, x-1)
        elif action == 'down':
            x = min(self.size-1, x+1)
        elif action == 'left':
            y = max(0, y-1)
        elif action == 'right':
            y = min(self.size-1, y+1)

        return (x, y)

    def get_reward(self, state, next_state):
        return self.rewards.get(next_state, 0)

def td0_policy_evaluation(grid, policy, gamma=0.9, alpha=0.1, episodes=1000):
    # Initialize value function
    V = np.zeros((grid.size, grid.size))

    for _ in range(episodes):
        # Start from a random non-terminal state
        while True:
            state = (np.random.randint(grid.size), np.random.randint(grid.size))
            if state not in grid.terminal_states:
                break

        while state not in grid.terminal_states:
            # Choose action according to policy
            action = policy(state)

            # Take action, observe next state and reward
            next_state = grid.get_next_state(state, action)
            reward = grid.get_reward(state, next_state)

            # TD(0) update
            V[state] += alpha * (reward + gamma * V[next_state] - V[state])

            state = next_state

    return V
            ''',
        10: '''
           import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# actions: hit or stand
ACTION_HIT = 0
ACTION_STAND = 1  #  "strike" in the book
ACTIONS = [ACTION_HIT, ACTION_STAND]

# policy for player
POLICY_PLAYER = np.zeros(22, dtype=int)
for i in range(12, 20):
    POLICY_PLAYER[i] = ACTION_HIT
POLICY_PLAYER[20] = ACTION_STAND
POLICY_PLAYER[21] = ACTION_STAND

# function form of target policy of player
def target_policy_player(usable_ace_player, player_sum, dealer_card):
    return POLICY_PLAYER[player_sum]

# function form of behavior policy of player
def behavior_policy_player(usable_ace_player, player_sum, dealer_card):
    if np.random.binomial(1, 0.5) == 1:
        return ACTION_STAND
    return ACTION_HIT

# policy for dealer
POLICY_DEALER = np.zeros(22)
for i in range(12, 17):
    POLICY_DEALER[i] = ACTION_HIT
for i in range(17, 22):
    POLICY_DEALER[i] = ACTION_STAND

# get a new card
def get_card():
    card = np.random.randint(1, 14)
    card = min(card, 10)
    return card

# get the value of a card (11 for ace).
def card_value(card_id):
    return 11 if card_id == 1 else card_id

# play a game
# @policy_player: specify policy for player
# @initial_state: [whether player has a usable Ace, sum of player's cards, one card of dealer]
# @initial_action: the initial action
def play(policy_player, initial_state=None, initial_action=None):
    # player status

    # sum of player
    player_sum = 0

    # trajectory of player
    player_trajectory = []

    # whether player uses Ace as 11
    usable_ace_player = False

    # dealer status
    dealer_card1 = 0
    dealer_card2 = 0
    usable_ace_dealer = False

    if initial_state is None:
        # generate a random initial state

        while player_sum < 12:
            # if sum of player is less than 12, always hit
            card = get_card()
            player_sum += card_value(card)

            # If the player's sum is larger than 21, he may hold one or two aces.
            if player_sum > 21:
                assert player_sum == 22
                # last card must be ace
                player_sum -= 10
            else:
                usable_ace_player |= (1 == card)

        # initialize cards of dealer, suppose dealer will show the first card he gets
        dealer_card1 = get_card()
        dealer_card2 = get_card()

    else:
        # use specified initial state
        usable_ace_player, player_sum, dealer_card1 = initial_state
        dealer_card2 = get_card()

    # initial state of the game
    state = [usable_ace_player, player_sum, dealer_card1]

    # initialize dealer's sum
    dealer_sum = card_value(dealer_card1) + card_value(dealer_card2)
    usable_ace_dealer = 1 in (dealer_card1, dealer_card2)
    # if the dealer's sum is larger than 21, he must hold two aces.
    if dealer_sum > 21:
        assert dealer_sum == 22
        # use one Ace as 1 rather than 11
        dealer_sum -= 10
    assert dealer_sum <= 21
    assert player_sum <= 21

    # game starts!

    # player's turn
    while True:
        if initial_action is not None:
            action = initial_action
            initial_action = None
        else:
            # get action based on current sum
            action = policy_player(usable_ace_player, player_sum, dealer_card1)

        # track player's trajectory for importance sampling
        player_trajectory.append([(usable_ace_player, player_sum, dealer_card1), action])

        if action == ACTION_STAND:
            break
        # if hit, get new card
        card = get_card()
        # Keep track of the ace count. the usable_ace_player flag is insufficient alone as it cannot
        # distinguish between having one ace or two.
        ace_count = int(usable_ace_player)
        if card == 1:
            ace_count += 1
        player_sum += card_value(card)
        # If the player has a usable ace, use it as 1 to avoid busting and continue.
        while player_sum > 21 and ace_count:
            player_sum -= 10
            ace_count -= 1
        # player busts
        if player_sum > 21:
            return state, -1, player_trajectory
        assert player_sum <= 21
        usable_ace_player = (ace_count == 1)

    # dealer's turn
    while True:
        # get action based on current sum
        action = POLICY_DEALER[dealer_sum]
        if action == ACTION_STAND:
            break
        # if hit, get a new card
        new_card = get_card()
        ace_count = int(usable_ace_dealer)
        if new_card == 1:
            ace_count += 1
        dealer_sum += card_value(new_card)
        # If the dealer has a usable ace, use it as 1 to avoid busting and continue.
        while dealer_sum > 21 and ace_count:
            dealer_sum -= 10
            ace_count -= 1
        # dealer busts
        if dealer_sum > 21:
            return state, 1, player_trajectory
        usable_ace_dealer = (ace_count == 1)

    # compare the sum between player and dealer
    assert player_sum <= 21 and dealer_sum <= 21
    if player_sum > dealer_sum:
        return state, 1, player_trajectory
    elif player_sum == dealer_sum:
        return state, 0, player_trajectory
    else:
        return state, -1, player_trajectory

# Monte Carlo Sample with On-Policy
def monte_carlo_on_policy(episodes):
    states_usable_ace = np.zeros((10, 10))
    # initialze counts to 1 to avoid 0 being divided
    states_usable_ace_count = np.ones((10, 10))
    states_no_usable_ace = np.zeros((10, 10))
    # initialze counts to 1 to avoid 0 being divided
    states_no_usable_ace_count = np.ones((10, 10))
    for i in tqdm(range(0, episodes)):
        _, reward, player_trajectory = play(target_policy_player)
        for (usable_ace, player_sum, dealer_card), _ in player_trajectory:
            player_sum -= 12
            dealer_card -= 1
            if usable_ace:
                states_usable_ace_count[player_sum, dealer_card] += 1
                states_usable_ace[player_sum, dealer_card] += reward
            else:
                states_no_usable_ace_count[player_sum, dealer_card] += 1
                states_no_usable_ace[player_sum, dealer_card] += reward
    return states_usable_ace / states_usable_ace_count, states_no_usable_ace / states_no_usable_ace_count

# Monte Carlo with Exploring Starts
def monte_carlo_es(episodes):
    # (playerSum, dealerCard, usableAce, action)
    state_action_values = np.zeros((10, 10, 2, 2))
    # initialze counts to 1 to avoid division by 0
    state_action_pair_count = np.ones((10, 10, 2, 2))

    # behavior policy is greedy
    def behavior_policy(usable_ace, player_sum, dealer_card):
        usable_ace = int(usable_ace)
        player_sum -= 12
        dealer_card -= 1
        # get argmax of the average returns(s, a)
        values_ = state_action_values[player_sum, dealer_card, usable_ace, :] / \
                  state_action_pair_count[player_sum, dealer_card, usable_ace, :]
        return np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])

    # play for several episodes
    for episode in tqdm(range(episodes)):
        # for each episode, use a randomly initialized state and action
        initial_state = [bool(np.random.choice([0, 1])),
                       np.random.choice(range(12, 22)),
                       np.random.choice(range(1, 11))]
        initial_action = np.random.choice(ACTIONS)
        current_policy = behavior_policy if episode else target_policy_player
        _, reward, trajectory = play(current_policy, initial_state, initial_action)
        first_visit_check = set()
        for (usable_ace, player_sum, dealer_card), action in trajectory:
            usable_ace = int(usable_ace)
            player_sum -= 12
            dealer_card -= 1
            state_action = (usable_ace, player_sum, dealer_card, action)
            if state_action in first_visit_check:
                continue
            first_visit_check.add(state_action)
            # update values of state-action pairs
            state_action_values[player_sum, dealer_card, usable_ace, action] += reward
            state_action_pair_count[player_sum, dealer_card, usable_ace, action] += 1

    return state_action_values / state_action_pair_count

# Monte Carlo Sample with Off-Policy
def monte_carlo_off_policy(episodes):
    initial_state = [True, 13, 2]

    rhos = []
    returns = []

    for i in range(0, episodes):
        _, reward, player_trajectory = play(behavior_policy_player, initial_state=initial_state)

        # get the importance ratio
        numerator = 1.0
        denominator = 1.0
        for (usable_ace, player_sum, dealer_card), action in player_trajectory:
            if action == target_policy_player(usable_ace, player_sum, dealer_card):
                denominator *= 0.5
            else:
                numerator = 0.0
                break
        rho = numerator / denominator
        rhos.append(rho)
        returns.append(reward)

    rhos = np.asarray(rhos)
    returns = np.asarray(returns)
    weighted_returns = rhos * returns

    weighted_returns = np.add.accumulate(weighted_returns)
    rhos = np.add.accumulate(rhos)

    ordinary_sampling = weighted_returns / np.arange(1, episodes + 1)

    with np.errstate(divide='ignore',invalid='ignore'):
        weighted_sampling = np.where(rhos != 0, weighted_returns / rhos, 0)

    return ordinary_sampling, weighted_sampling

def figure_5_1():
    states_usable_ace_1, states_no_usable_ace_1 = monte_carlo_on_policy(10000)
    states_usable_ace_2, states_no_usable_ace_2 = monte_carlo_on_policy(500000)

    states = [states_usable_ace_1,
              states_usable_ace_2,
              states_no_usable_ace_1,
              states_no_usable_ace_2]

    titles = ['Usable Ace, 10000 Episodes',
              'Usable Ace, 500000 Episodes',
              'No Usable Ace, 10000 Episodes',
              'No Usable Ace, 500000 Episodes']

    _, axes = plt.subplots(2, 2, figsize=(40, 30))
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    axes = axes.flatten()

    for state, title, axis in zip(states, titles, axes):
        fig = sns.heatmap(np.flipud(state), cmap="YlGnBu", ax=axis, xticklabels=range(1, 11),
                          yticklabels=list(reversed(range(12, 22))))
        fig.set_ylabel('player sum', fontsize=30)
        fig.set_xlabel('dealer showing', fontsize=30)
        fig.set_title(title, fontsize=30)

    plt.savefig('figure_5_1.png')
    plt.close()

def figure_5_2():
    state_action_values = monte_carlo_es(500000)

    state_value_no_usable_ace = np.max(state_action_values[:, :, 0, :], axis=-1)
    state_value_usable_ace = np.max(state_action_values[:, :, 1, :], axis=-1)

    # get the optimal policy
    action_no_usable_ace = np.argmax(state_action_values[:, :, 0, :], axis=-1)
    action_usable_ace = np.argmax(state_action_values[:, :, 1, :], axis=-1)

    images = [action_usable_ace,
              state_value_usable_ace,
              action_no_usable_ace,
              state_value_no_usable_ace]

    titles = ['Optimal policy with usable Ace',
              'Optimal value with usable Ace',
              'Optimal policy without usable Ace',
              'Optimal value without usable Ace']

    _, axes = plt.subplots(2, 2, figsize=(40, 30))
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    axes = axes.flatten()

    for image, title, axis in zip(images, titles, axes):
        fig = sns.heatmap(np.flipud(image), cmap="YlGnBu", ax=axis, xticklabels=range(1, 11),
                          yticklabels=list(reversed(range(12, 22))))
        fig.set_ylabel('player sum', fontsize=30)
        fig.set_xlabel('dealer showing', fontsize=30)
        fig.set_title(title, fontsize=30)

    plt.savefig('figure_5_2.png')
    plt.close()

def figure_5_3():
    true_value = -0.27726
    episodes = 10000
    runs = 100
    error_ordinary = np.zeros(episodes)
    error_weighted = np.zeros(episodes)
    for i in tqdm(range(0, runs)):
        ordinary_sampling_, weighted_sampling_ = monte_carlo_off_policy(episodes)
        # get the squared error
        error_ordinary += np.power(ordinary_sampling_ - true_value, 2)
        error_weighted += np.power(weighted_sampling_ - true_value, 2)
    error_ordinary /= runs
    error_weighted /= runs

    plt.plot(np.arange(1, episodes + 1), error_ordinary, color='green', label='Ordinary Importance Sampling')
    plt.plot(np.arange(1, episodes + 1), error_weighted, color='red', label='Weighted Importance Sampling')
    plt.ylim(-0.1, 5)
    plt.xlabel('Episodes (log scale)')
    plt.ylabel(f'Mean square error\n(average over {runs} runs)')
    plt.xscale('log')
    plt.legend()

    plt.savefig('figure_5_3.png')
    plt.close()


if __name__ == '__main__':
    figure_5_1()
    figure_5_2()
    figure_5_3()
    from IPython.display import Image
display(Image(filename='figure_5_1.png'))
display(Image(filename='figure_5_2.png'))
display(Image(filename='figure_5_3.png'))
            '''

    }

    return switcher.get(selection, "Invalid selection")


