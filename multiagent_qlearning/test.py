#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from simpleMaze import Maze
from matplotlib import pyplot as plt
from sklearn.externals import joblib

env = Maze(n_goals = 2,
            n_agents = 2,
            origin_random=True)
t1=time.time()
RL = joblib.load('table2.pkl')
print(RL.q_table.size)
print(time.time()-t1)
RL.epsilon=0.80
REWARD = [] 
STEP = [] 
num=10
UNIT = 40
def update(num):
    for episode in range(num):
        observation = env.reset()
        sum_reward = 0
        step = 0
        while True:
            time.sleep(0.17)
            env.update()
            action = RL.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            sum_reward += reward
            step += 1
            observation = observation_
            if done:
                REWARD.append(sum_reward)
                STEP.append(step)
                print('episode' + str(episode+1) + ' sum_reward :' + str(int(sum_reward)) + '; number of step :' + str(step))               
                break
            
env.after(100, update(num))
env.mainloop()
plt.plot(range(1,len(REWARD)+1),REWARD)
plt.show()
