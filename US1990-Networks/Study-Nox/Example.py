import pandas as pd
from BetterUIMNIST import * 

#This is an example Neural Network, Just Run this file and the example will work

InputData = pd.read_csv('Input.csv', sep=" ").to_numpy().tolist()
OutputData = pd.read_csv('Output.csv', sep=" ").to_numpy().tolist()


for buhj in range(20):
    NNFrame = NeuralFrame([2, 23, 23, 67], [CalcCost, Swish, Swish, Swish])
    MakeTxT(NNFrame)

    NeuralNetwork(InputData[0:25000], OutputData[0:25000], 250, 100, 0.045)
    TestingNetwork(InputData[50000:60000], OutputData[50000:60000], 100, 100, "Swish")


for buheeeej in range(20):
    NNFrame = NeuralFrame([2, 23, 23, 67], [CalcCost, Relu, Relu, Relu])
    MakeTxT(NNFrame)

    NeuralNetwork(InputData[0:25000], OutputData[0:25000], 250, 100, 0.045)
    TestingNetwork(InputData[50000:60000], OutputData[50000:60000], 100, 100, "Relu")


for ijediej in range(20):
    NNFrame = NeuralFrame([2, 23, 23, 67], [CalcCost, Tanh, Tanh, Tanh])
    MakeTxT(NNFrame)

    NeuralNetwork(InputData[0:25000], OutputData[0:25000], 250, 100, 0.045)
    TestingNetwork(InputData[50000:60000], OutputData[50000:60000], 100, 100, "Tanh")




