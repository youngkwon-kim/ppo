#*-* coding: utf-8 *-*
import pandas as pd


class Env():
    def __init__(self):
        self.cnt = 0
        self.pre_a = 0
        self.done = False
        self.env_data = pd.read_csv("KOSPI_F_30_1.csv")

    def reset(self):
        self.cnt = 0
        self.pre_a = 0

    def getOnes(self):
        self.cnt = self.cnt + 1
        return self.env_data.iloc[self.cnt].values
     
    def step(self, a):
        if(self.pre_a == a):
            r = 0
        elif(a == 0):
            r = 0
        else:
            r = -1

        if(a != 0):
            self.pre_a = a
        s_prime = self.getOnes()
        return s_prime, r

if __name__ == '__main__':
    env = Env()
    env.reset()
    for a in [1,0,2,2,0,0,0,0,0,1,2,2,0,1,1,1,2]:
        st = env.step(a)
        print(st)