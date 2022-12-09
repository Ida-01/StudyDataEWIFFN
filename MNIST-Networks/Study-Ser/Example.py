from mnist import MNIST
from BetterUIMNIST import * 

#This is an example Neural Network, Just Run this file and the example will work

mndata = MNIST('samples')

images, labels = mndata.load_training()

InputOG = images



InputData = []
for Things in InputOG:
    newli = []
    for uijk in Things:
        newli.append(uijk/255)
    InputData.append(newli)

OutputData = []
for Numb in labels:
    OutputData.append(CalcExpe(Numb))



NNFrame = NeuralFrame([10, 40, 40, 784], [CalcCost, Swish, Swish, Swish])
MakeTxT(NNFrame)

NeuralNetwork(InputData[0:25000], OutputData[0:25000], 250, 100, 0.045)
TestingNetwork(InputData[50000:60000], OutputData[50000:60000], 100, 100, "Swish")



#NeuralNetwork(InputData[0:48000], OutputData[0:48000], 300, 100, 0.045)
#TestingNetwork(InputData[48000:60000], OutputData[48000:60000], 3, 50)
#print(np.argmax(UseNetwork(InputData[49533])))




