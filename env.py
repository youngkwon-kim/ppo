#*-* coding: utf-8 *-*
import pandas as pd
import numpy as np
import torch
import pickle

class Env():
    def __init__(self):
        self.cnt = 0
        self.pre_a = 0      # call(put medo) : 1, put(call medo) : 2, none : 0
        self.done = False
        self.position = 0.0   # call position : 1, put position : -1, none position : 0
        self.position_value = 0.0
        self.total = 0.0
        self.lossCut = 0.5
        self.env_data = pd.read_csv("KOSPI_F_30_1.csv").dropna()
        self.env_data = self.env_data.sort_index(ascending=False)

    def reset(self):
        #self.cnt = 0
        self.pre_a = 0
        self.done = False
        s_prime = self.getOnes()
        sp = [s_prime[5],s_prime[10],s_prime[11],s_prime[12],(s_prime[10] - s_prime[12]), 0.0]
        sp3 = np.array(sp)
        #print(sp)
        return sp3

    def getOnes(self):
        self.cnt = self.cnt + 1
        return self.env_data.iloc[self.cnt].values
     
    def step(self, a):
        self.info = ""
        s_prime = self.getOnes()
        #sp.append([s_prime[5],s_prime[10],s_prime[11],s_prime[12],(s_prime[10] - s_prime[12])])
        sp = [s_prime[5],s_prime[10],s_prime[11],s_prime[12],(s_prime[10] - s_prime[12])]
        reword = round((s_prime[5] - self.position_value) * 1, 1)

        if(self.pre_a == a or a == 0):
            r = 0
            if(self.position == 1):
                if(reword < -self.lossCut):
                    self.position = 0
                    self.position_value = 0
                    self.done = True
                    r = reword
                    self.info = "콜자손"
            if(self.position == -1):
                if(reword > self.lossCut):
                    self.position = 0
                    self.position_value = 0
                    self.done = True
                    r = -reword
                    self.info = "풋자손"
        elif(self.pre_a != a):
            r = -1
            if(self.position == 0):
                if(a == 1): 
                    self.position = 1
                    self.position_value = float(s_prime[5])
                    self.info = "콜진입"
                if(a == 2): 
                    self.position = -1
                    self.position_value = float(s_prime[5])
                    self.info = "풋진입"
            elif(self.position == 1):
                if(self.pre_a == 1):
                    self.position = 0
                    self.position_value = 0
                    self.done = True
                    r = reword
                    self.info = "콜손절"
            elif(self.position == -1):
                if(self.pre_a == 2):
                    self.position = 0
                    self.position_value = 0
                    self.done = True
                    r = -reword
                    self.info = "풋손절"

        sp.append(self.position)
        sp2 = np.array(sp)
        #print(torch.from_numpy(sp2).float())
        if(a != 0):
            self.pre_a = a
        self.total = self.total + r
        return sp2, r, self.done, self.position

if __name__ == '__main__':
    env = Env()
    s = env.reset()
    print(s)
    for a in [1,2,1,2,1,2,2,2,1,2,0,0,1,2,1,2,2,2,0,0,1,1,1,2]:
        sp,r,done,posiotion = env.step(a)
        print(sp,r,done,posiotion)
        if(done == True):
            env.reset()