#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import time
import random
import tkinter as tk

#One Goal
UNIT = 40
DEFAULT_MAP = np.array([[0,0,0,0,0,0],
                         [0,0,-1,-1,0,0],
                         [0,-1,1,0,0,0],                   
                         [0,-1,0,1,-1,0],
                         [0,0,0,-1,0,0],
                         [0,0,0,0,0,1]])#1:Goal;-1:block
class Maze(tk.Tk, object):
    def __init__(
            self,
            Map=DEFAULT_MAP,
            n_goals = 3,
            n_agents = 3,
            origin_random=False):
        super(Maze, self).__init__()
        global MAZE_H,MAZE_W
        self.title('maze')
        self.map = Map
        MAZE_W = self.map.shape[1]
        MAZE_H = self.map.shape[0]        
        self.n_goals = n_goals
        self.n_agents = n_agents
        self.n_actions = 5**n_agents
        
        self.blocks = []
        self.ovals = []#goal 
        self.rects = []#agent
        
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT+UNIT, MAZE_H * UNIT+UNIT))
        self.origin_random = origin_random # if True ,agents start position is random
        
        self.build_maze()
            
    def build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)
        button = tk.Button(self,text='Exit',command=self.quit)
        button.pack()
        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1) # canvas axis is (width,height)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        
        # create blocks
        for (x,y) in list(zip(np.where(self.map==-1)[0],np.where(self.map==-1)[1])):
            self.blocks.append(self.canvas.create_rectangle(
            y*UNIT + 5, x*UNIT + 5,
            y*UNIT + 35, x*UNIT + 35,
            fill='black'))        
        
        # create goal
        self.map[np.where(self.map==1)[0][self.n_goals:],np.where(self.map==1)[1][self.n_goals:]]=0 # for situation n_goals is smaller than the num of '1' in the map
        self.goal = list(zip(np.where(self.map==1)[0],np.where(self.map==1)[1]))
        for (x,y) in self.goal:
            self.ovals.append(self.canvas.create_oval(
                y*UNIT + 5, x*UNIT + 5,
                y*UNIT +35, x*UNIT + 35,
                fill='yellow'))

        self.creat_agent()
        self.canvas.pack()
    
    def reset(self):
        self.update()
#        time.sleep(0.0000001)# help you see the finished status
        for i in range(self.n_agents):
            self.canvas.delete(self.rects[i])
        self.rects = []
        return self.creat_agent()
    
    def creat_agent(self): 
        # default original position
        self.origin = list(zip(np.where(self.map==0)[0],np.where(self.map==0)[1]))[:self.n_agents] 
        # random original position
        if self.origin_random: 
            sites = random.sample(list(zip(np.where(self.map==0)[0],np.where(self.map==0)[1])),self.n_agents)
            for i,site in enumerate(sites):
                self.origin[i] = sites[i] 
        # create agents
        for i in range(self.n_agents):
            self.rects.append(self.canvas.create_rectangle(
            self.origin[i][1]*UNIT + 5, self.origin[i][0]*UNIT + 5,
            self.origin[i][1]*UNIT + 35, self.origin[i][0]*UNIT + 35,
            fill='red'))
        return self.origin
    
    def step(self, action): 
        s = []
        s_ = []
        dones = [False]*self.n_agents
        done = False
        reward = 0
        base_action = np.array([[0, 0]]*self.n_agents)    
        for rect in self.rects:
            pos = self.canvas.coords(rect)
            s_y = int((pos[0]/UNIT+pos[2]/UNIT-1)/2)
            s_x = int((pos[1]/UNIT+pos[3]/UNIT-1)/2)
            s.append((s_x,s_y))        

        for i,rect in enumerate(self.rects):
            #already reached goal
            if s[i] in list(zip(np.where(self.map==1)[0],np.where(self.map==1)[1])):
                dones[i] = True
                s_.append(s[i])
                
            else:
                action_=action//(5**i)%5 #action is base-10 system ,transfer to base-5
                pos = self.canvas.coords(rect)
                if action_ == 0:   # up
                    if pos[1] > UNIT:
                        base_action[i][0] -= 1
                elif action_ == 2:   # down
                    if pos[1] < (MAZE_H - 1) * UNIT:
                        base_action[i][0] += 1
                elif action_ == 1:   # right
                    if pos[0] < (MAZE_W - 1) * UNIT:
                        base_action[i][1] += 1
                elif action_ == 3:   # left
                    if pos[0] > UNIT:
                        base_action[i][1] -= 1  
                else:# action_ == 4:
#                    print("rect",i,":Keep status")
                    reward+=4
                    
                if base_action[i][0]==base_action[i][1]:
#                    print("rect",i,": Hit boundary or keep status")
                    reward-=4
                    s_.append(s[i])
                
                else:
                    site_ = tuple(s[i]+base_action[i])   
                    # next station is goal
                    if site_ in list(zip(np.where(self.map==1)[0],np.where(self.map==1)[1])):
                        if site_ in s: # already have agent reach this goal
                            base_action[i] = np.array([0, 0])
                        else:
                            reward += 100
                            dones[i]=True
#                            print("rect",i,":Finished")
                    elif site_ in list(zip(np.where(self.map==-1)[0],np.where(self.map==-1)[1])):#hit block
                        reward -= 4
                        base_action[i] = np.array([0, 0])
#                        print("rect",i,":Hit block")
                    else:
                        # hit lower priority agent's old state or hit higher agent's current state
                        if site_ in s[i:] or site_ in s_[:i]:
                            reward -= 4
                            base_action[i] = np.array([0, 0])
                        # walking without any obstruct
                        else:
                            reward-=1                            
                            
                    s_.append(tuple(s[i]+base_action[i]))
                    self.canvas.move(rect, base_action[i][1]*UNIT, base_action[i][0]*UNIT) 
        
        if all(dones):# all agents have reached goal
            done = True
            
        return s_, reward, done 
 
    def render(self):
        self.update()

if __name__ == '__main__':
    env = Maze(origin_random=True)
    step = 0
    while True:
        step+=1
        env.render()
        observation_, reward, done = env.step(np.random.randint(125))
        if done:
            break
    
    env.mainloop()
    print(step)
