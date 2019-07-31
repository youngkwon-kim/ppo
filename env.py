#*-* coding: utf-8 *-*
import pandas as pd
import pickle

class Env():
    def __init__(self):
        self.cnt = 0
        self.pre_a = 0      # call(put medo) : 1, put(call medo) : 2, none : 0
        self.done = False
        self.position = 0   # call position : 1, put position : -1, none position : 0
        self.position_value = 0.0
        self.total = 0.0
        self.env_data = pd.read_csv("KOSPI_F_30_1.csv").dropna()
        self.env_data = self.env_data.sort_index(ascending=False)

    def reset(self):
        #self.cnt = 0
        self.pre_a = 0
        self.done = False
        self.cnt = self.cnt + 1
        return self.env_data.iloc[self.cnt].values

    def getOnes(self):
        self.cnt = self.cnt + 1
        return self.env_data.iloc[self.cnt].values
     
    def step(self, a):
        self.info = ""
        s_prime = self.getOnes()
        sp = []
        sp.append(s_prime[5])

        reword = round((s_prime[5] - self.position_value) * 1, 2)

        if(self.pre_a == a):
            r = 0
            if(self.position == 1):
                if(reword < -0.5):
                    self.position = 0
                    self.position_value = 0
                    self.done = True
                    r = reword
                    self.info = "콜자손"
            if(self.position == -1):
                if(reword > 0.5):
                    self.position = 0
                    self.position_value = 0
                    self.done = True
                    r = -reword
                    self.info = "풋자손"
        elif(a == 0):
            r = 0
            if(self.position == 1):
                if(reword < -0.5):
                    self.position = 0
                    self.position_value = 0
                    self.done = True
                    r = reword
                    self.info = "콜자손"
            if(self.position == -1):
                if(reword > 0.5):
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

        if(a != 0):
            self.pre_a = a
        self.total = self.total + r
        return sp, r, self.done, self.position, self.position_value, self.info, self.total

if __name__ == '__main__':
    env = Env()
    s = env.reset()
    for a in [1,0,1,0,1,1,1,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2]:
        sp,r,done,posiotion,position_value, info, total = env.step(a)
        print(sp,r,done,posiotion,position_value, info, total)
        if(done == True):
            env.reset()