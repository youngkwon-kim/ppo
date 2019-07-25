import pandas as pd


class Env():
    def __init__(self):
        self.env_data = pd.read_csv("KOSPI_F_30_1.csv")

    def getOnes(self):
        pass
        
if __name__ == '__main__':
    Env()