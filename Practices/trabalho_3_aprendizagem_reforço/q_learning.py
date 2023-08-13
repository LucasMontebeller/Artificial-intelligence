# Cart pole
import gymnasium as gym
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np

env = gym.make('CartPole-v1', render_mode='rgb_array')

# # Aleatório
# episodes = 5
# for episode in range(1, episodes+1):
#     score = 0.0
#     # Reinicializar o ambiente
#     state = env.reset()
#     print(state)

#     print('Episodio: ', episode)
#     # Executar a simulação
#     terminated = False
#     while not terminated:
#         # Renderizar o ambiente
#         img = env.render()

#         # Plota o quadro
#         plt.imshow(img)     #####
#         plt.axis('off')     ####3
#         plt.show()

#         # Tomar uma ação
#         # 0 - Esquerda
#         # 1 - Direita
#         action = env.action_space.sample()

#         # Executar a ação no ambiente
#         next_state, reward, terminated, truncated, info = env.step(action)
#         score += reward

#         done = terminated or truncated

#         #clear_output(wait=True) #####
#         #plt.pause(0.0001)       #####

#         print('\t', score, next_state, reward, terminated, truncated, info)

# # Fechar o ambiente
# env.close()


import numpy as np

class StateAction:
    def __init__(self, state, action):
        self.state = state
        self.action = action
        self.q_value = 0.0

def main():
    EPISODES = 5
    GAMMA = 0.99
    ALPHA = 0.1
    EXPLORATION_DECAY = 0.01
    exploration_prob = 1

    # lista com StateAction
    state_actions = set()

    def choose_action(state):
        if np.random.uniform(0, 1) < exploration_prob:
            return env.action_space.sample()
        else:
            return np.argmax([pair.q_value for pair in state_actions if np.all(pair.state == state)])

    def update_Q(state, action, reward, next_state):
        for pair in state_actions:
            if np.all(pair.state == state) and pair.action == action:
                max_next_state = max([pair.q_value for pair in state_actions if np.all(pair.state == next_state)] or [0])
                pair.q_value = (1 - ALPHA) * pair.q_value + ALPHA * (reward + GAMMA * max_next_state)
                break

    for episode in range(EPISODES):
        score = 0.0
        state = env.reset()

        print('Episode:', episode)
        while True:
            img = env.render()
            plt.imshow(img)
            plt.axis('off')
            # plt.show()

            action = choose_action(state)
            state_actions.add(StateAction(state, action))
            next_state, reward, terminated, truncated, info = env.step(action)

            update_Q(state, action, reward, next_state)
            score += reward

            state = next_state

            print('\t', score, next_state, reward, terminated, truncated, info)

            if terminated or truncated:
                break
    
        exploration_prob = np.exp(-EXPLORATION_DECAY)

    # Fechar o ambiente
    env.close()

if __name__ == '__main__':
    main()