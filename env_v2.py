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
        info, s_prime = self.getOnes()
        if(info):
            sp = [s_prime[0],s_prime[1],s_prime[2],s_prime[3],(s_prime[4] - s_prime[5]), 0]
        else:
            sp = [0,0,0,0,0,0]
        sp3 = np.array(sp)
        #print(sp)
        return sp3

    def getOnes(self):
        try:
            self.cnt = self.cnt + 1
            sp = self.env_data.iloc[self.cnt].values
            # sp[0] = End Value
            re = [True, [sp[0],sp[1],sp[2],sp[3],(sp[4] - sp[5])]]
        except:
            re = [False,[0,0,0,0,0]]
        return re
     
    def step(self, a):
        info, s_prime = self.getOnes()

        if(info):
            pass
        else:
            pass



        sp.append(self.position)
        sp2 = np.array(sp)
        #print(torch.from_numpy(sp2).float())
        if(a != 0):
            self.pre_a = a
        self.total = self.total + reword
        return sp2, r, self.done, info

if __name__ == '__main__':
    env = Env()
    s = env.reset()
    print(s)
    for a in [1,2,1,2,1,2,2,2,1,2,0,0,1,2,1,2,2,2,0,0,1,1,1,2]:
        sp,r,done,posiotion = env.step(a)
        print(sp,r,done,posiotion)
        if(done == True):
            env.reset()