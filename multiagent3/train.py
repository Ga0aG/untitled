#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from simpleMaze import Maze
from brain import QLearningTable
from matplotlib import pyplot as plt
from sklearn.externals import joblib
import tqdm

def update(num):
    for episode in tqdm.tqdm(range(num)):
        observation = env.reset()
        sum_reward = 0
        step = 0
        RL.learning_rate = lr[episode]
        while True:
            env.render() #env.update()
            action = RL.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            sum_reward += reward
            step += 1
            RL.learn(str(observation), action, reward, str(observation_),done)
            observation = observation_
            if done:
                REWARD.append(sum_reward)
                STEP.append(step)
                #print('episode' + str(episode+1) + ' sum_reward :' + str(int(sum_reward)) + '; number of step :' + str(step))               
#                print(RL.q_table)
                break

REWARD = [] 
STEP = [] 
lr = [0.1]*200+[0.03]*250+[0.005]*400+[0.0005]*400#+[0.0001]*400#+[0.00001]*400

env = Maze( n_goals = 2,
            n_agents = 2,
            origin_random=True,
            interval = 0.00000001) #random needs more training
RL = QLearningTable(actions=list(range(env.n_actions)))
env.after(100, update(len(lr)))
env.mainloop()
joblib.dump(RL,'table2.pkl')
plt.plot(range(1,len(REWARD)+1),REWARD)
plt.show()
