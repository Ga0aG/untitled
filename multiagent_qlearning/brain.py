#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


class QLearningTable:
    def __init__(self, actions, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  
        self.lr = learning_rate 
        self.gamma = reward_decay   
        self.epsilon = e_greedy    
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)   
        self.error_function = []
        self.q_target = []
        self.q_predict = []
    
    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [-1]*len(self.actions), # -1 seems better than 0
                    index=self.q_table.columns,
                    name=state,
                )
            )    
    
    def choose_action(self, observation):
        self.check_state_exist(observation) 
        if np.random.uniform() <= self.epsilon:  
            state_action = self.q_table.loc[observation, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:   
            action = np.random.choice(self.actions)
        return action
    
    def learn(self, s, a, r, s_, done):
        self.check_state_exist(s_)  
        q_predict = self.q_table.loc[s, a] 
        if done:
            q_target = r 
        else:
            q_target = r + self.gamma * self.q_table.loc[s_, :].max() 
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  
        
        #error each episode 保留四位小数round函数
        self.error_function.append(round((q_target - q_predict) ** 2,4))
        self.q_predict.append(round(q_predict,4))
        self.q_target.append(round(q_target,4))
    

