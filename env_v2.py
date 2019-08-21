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
        self.position = False   # call position : 1, put position : -1, none position : 0
        self.position_value = {}
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
            sp = [0,0,0,0,0,0]
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
        print(self.cnt, sp[0])
        return re

    def step(self, a):
        info, s_prime = self.getOnes()
        reword = 0

        if(info):
            if(self.position):
                pass
            else:
                self.position_value["code"] = s_prime[0]
        else:
            pass

        s_prime.append(self.position)
        sp2 = np.array(s_prime)
        #print(torch.from_numpy(sp2).float())
        if(a != 0):
            self.pre_a = a
        #self.total = self.total + reword
        return sp2, reword, self.done, info

if __name__ == '__main__':
    env = Env()
    s = env.reset()
    print(s)
    for i in range(30):
        for a in [1,2,1,2,1,2,2,2,1,2,0,0,1,2,1,2,2,2,0,0,1,1,1,2]:
            sp,r,done,info = env.step(a)
            print(sp,r,done,info)
            if(done == True):
                env.reset()