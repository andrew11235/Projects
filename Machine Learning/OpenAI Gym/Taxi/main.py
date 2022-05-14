import gym
import numpy as np


def zero_q_table(env):
    return np.zeros([env.observation_space.n, env.action_space.n])


def load_q_table(filename):
    with open(filename, 'r') as f:
        q = np.loadtxt(f)
    return q


def save_q_table(filename, q_table):
    with open(filename, 'w') as f:
        np.savetxt(f, q_table)


def train(env, q_table, alpha, gamma, epsilon, iterations, simulate=False):
    for i in range(1, iterations + 1):
        state = env.reset()
        epochs, total_reward = 0, 0

        done = False

        while not done:
            if simulate:
                env.render()
                print(epochs, total_reward)

            if np.random.random() < epsilon:
                action = env.action_space.sample()  # Explore action space
            else:
                action = np.argmax(q_table[state])  # Exploit learned values

            next_state, reward, done, _ = env.step(action)

            total_reward += reward

            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, action] = new_value

            state = next_state

            epochs += 1

        if i % 5000 == 0:
            print(i)

    if simulate:
        env.render()
        print(epochs, total_reward)


def try_random(env):
    state = env.reset()
    epochs, total_reward = 0, 0

    done = False

    while not done:
        env.render()
        print(epochs, total_reward)

        action = env.action_space.sample()  # Explore action space

        next_state, reward, done, _ = env.step(action)
        total_reward += reward

        state = next_state

        epochs += 1

    env.render()
    print(epochs, total_reward)


def main():
    env = gym.make("Taxi-v3").env

    try:
        q_table = load_q_table('q_table.csv')
    except FileNotFoundError:
        q_table = zero_q_table(env)

    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1

    # try_random(env)

    train(env, q_table, alpha, gamma, epsilon, 100_000)

    save_q_table('q_table.csv', q_table)


if __name__ == '__main__':
    main()
