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
        self.linescale = 0
        self.env_data = pd.read_csv("KOSPI_F_30_2.csv").dropna()
        self.env_data = self.env_data.sort_index(ascending=False)
        self.linescale, _ = self.env_data.shape

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
        try:
            self.cnt = self.cnt + 1
            re = [True, self.env_data.iloc[self.cnt].values]
        except:
            re = [False,[]]
        return re
     
    def step(self, a):
        res, s_prime = self.getOnes()

        if(res):
            sp = [s_prime[5],s_prime[10],s_prime[11],s_prime[12],(s_prime[10] - s_prime[12])]
            reword = round((s_prime[5] - self.position_value) * 1, 1)



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