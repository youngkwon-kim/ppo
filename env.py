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
        s_prime = self.getOnes()
        if(self.pre_a == a):
            r = 0
        elif(a == 0):
            r = 0
        else:
            r = -1
            if(self.position == 0):
                if(a == 1): 
                    self.position = 1
                    self.position_value = float(s_prime[5])
                if(a == 2): 
                    self.position = -1
                    self.position_value = float(s_prime[5])
            elif(self.position == 1):
                if(self.pre_a == 1):
                    # 익절과 손절의 평가 필요
                    self.position = 0
                    self.done = True
                    if(s_prime[5] < (self.position_value - 0.2)):
                        r = -10
                    else:
                        r = (s_prime[5] - self.position_value) * 10
                    self.position_value = 0
            elif(self.position == -1):
                if(self.pre_a == 2):
                    #익절과 손절의 평가 필요
                    self.position = 0
                    self.done = True
                    if(s_prime[5] > (self.position_value - 0.2)):
                        r = -10
                    else:
                        r = (s_prime[5] - self.position_value) * 10
                    self.position_value = 0

        if(a != 0):
            self.pre_a = a
        
        return s_prime, r, self.done, self.position, self.position_value

if __name__ == '__main__':
    env = Env()
    s = env.reset()
    for a in [1,0,2,0,0,2,0,0,0,1,2,2,0,1,1,1,2,0,0,0,0,1,1,2,0,0,0,2,0,0,2,0,0,0,0,0,0,1,1,1,0,0,0,2,2,2]:
        sp,r,done,posiotion,position_value = env.step(a)
        print(sp,r,done,posiotion,position_value)
        if(done == True):
            env.reset()