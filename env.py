import pandas as pd


class Env():
    def __init__(self):
        self.env_data = pd.read_csv("KOSPI_F_30_1.csv")

    def reset(self):
        pass

    def getOnes(self):
        pass
        
    def step(self, a):
        if(a == 0):
            r = 0
        elif(a == 1):
            r = -1
        elif(a == 2):
            r = -1

if __name__ == '__main__':
    env = Env()
    env.reset()
    a = 1
    st = env.step(a)