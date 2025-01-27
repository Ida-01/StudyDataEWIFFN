import random
import math
import sys
import json
import numpy as np

class Setter():
    def __init__(self):
        NetWorkFrame = open("NetworkInfo.json", "r")
        OpenFrame = json.load(NetWorkFrame)
        NetWorkFrame.close()
        self.Neurons = OpenFrame['Neurons']
        exec('self.Activtions = ' + OpenFrame["Activtions"])
        exec('self.CostFunction = ' + OpenFrame["CostFunction"])
        self.Pooling = OpenFrame['Pooling']
        self.Chunk = OpenFrame['Chunk']
        exec('self.LoadingBar = ' + OpenFrame["LoadingBar"])
        exec('self.Filters = ' + OpenFrame["Filters"])
        exec('self.FiltFun = ' + OpenFrame["FiltFun"])
        KFrame = open("Kernals/AllKernals.json", "r")
        OpenKFrame = json.load(KFrame)
        KFrame.close()
        exec('self.Kernals = ' + OpenKFrame["Kernals"])

        KFrame = open("Kernals/BlankKerns.json", "r")
        OpenKFrame = json.load(KFrame)
        KFrame.close()
        exec('self.BlaKernals = ' + OpenKFrame["Kernals"])


class Kset:
    def __init__(self, *arg):

        self.number = arg[0]
        self.size = arg[1]
        if(len(arg) == 3):
            self.act = arg[2]
        else:
            self.act = Linear


#This is a NeuralFrame, It is used for Compressing Data in Parameters
class NeuralFrame:

    def __init__(self, ParNeur, ParActi):
        self.NeurList = ParNeur
        self.ActivList = ParActi
        self.ActivName = []
        self.CostFun = self.ActivList.pop(0)
        self.PoolNumb = 0
        self.ChunkNumb = 0


        for i in range(len(ParActi)):
            try:
                self.ActivName.append(ParActi[i].__name__)
            except:
                self.ActivName.append(ParActi[i])
        self.ActivName = str(self.ActivName).replace("'", "").replace("Pool", "'Pool'")



        self.loadbar = LoadingBarPre
        self.Filters = []
        self.Kernals = []
        self.KernalFun = []

    def SetCusLoad(self, load):
        self.loadbar = load
        return self

    def SetFilters(self, NewFilter):
        self.Filters = NewFilter
        self.Filters.reverse()
        return self

    def SetKernals(self, NewKernals):
        self.Kernals = NewKernals
        for i in NewKernals:
            try:
                self.KernalFun.append(i[2])
            except:
                self.KernalFun.append(Linear)

        KernalFunLI = []
        for fu in self.KernalFun:
                KernalFunLI.append(fu.__name__)
        self.KernalFun = str(KernalFunLI).replace("'", "")
        return self



def BlankKernal(KernLis):
    BKerns = []
    for kr in KernLis:
        NewBK = []
        for cde in range(len(kr)):
            NewBK.append(np.zeros((len(kr[cde]),len(kr[cde]))).tolist())
        BKerns.append(NewBK)
    return BKerns



def AddKernal(NewKerns, OldKerns, div):
    for i in range(len(NewKerns)):
        for j in range(len(NewKerns[i])):
            for k in range(len(NewKerns[i][j])):
                for o in range(len(NewKerns[i][j][k])):
                    for q in range(len(NewKerns[i][j][k])):
                        OldKerns[i][j][k][o][q] += (NewKerns[i][j][k][o][q]/div)
                    
    NewKData = json.loads('{"Kernals": 0}')
    NewKData['Kernals'] = str(OldKerns)
    OpeKnFile = open("Kernals/AllKernals.json", "w")
    json.dump(NewKData, OpeKnFile)
    OpeKnFile.close()


def PoolBackProp(Kw, Kh, Image, PrevGradient):
    NewGrad = np.zeros((len(Image[0]),len(Image[0]))).tolist()
    PrevGradInd = 0
    for i in range(len(Image) - (Kh - 1)): 
        for j in range(len(Image[0]) - (Kw - 1)):
            if (i + Kh) <= len(Image) and (j + Kw) <= len(Image[0]):

                max = Image[i][j]
                maxpos = (i,j)
                for r in range(Kh):
                    for c in range(Kw):
                        if Image[i + r][j + c] > max:
                            max = Image[i + r][j + c]
                            maxpos = (i + r, j + c)

                NewGrad[maxpos[0]][maxpos[1]] += PrevGradient[PrevGradInd]
                PrevGradInd += 1

    return NewGrad


def CombineGrids(GridList):
    NewGrid = np.zeros((len(GridList[0]), len(GridList[0][0]))).tolist()

    for l in range(len(GridList)): 

        for i in range(len(GridList[0])): 

            for j in range(len(GridList[0][0])): 

                NewGrid[i][j] += GridList[l][i][j]

    for i in range(len(GridList[0])): 
        for j in range(len(GridList[0][0])): 
            NewGrid[i][j] = NewGrid[i][j]/len(GridList)

    return NewGrid

def Convolution(Image, IMGfilter):
    NewIMG = []
    Image = Chunk(Image, int(math.sqrt(len(Image))))
    #Image = np.pad(Image, ((1,1),(1,1)), 'constant').tolist()
    FiltLen = len(IMGfilter)
    for i in range(0, len(Image) - (FiltLen - 1)):

        NewRow = []
        for j in range(0, len(Image[0]) - (FiltLen - 1)):
            Total = 0

            for r in range(0,FiltLen):
                for c in range(0,FiltLen):

                    Total += Image[i+r][j+c] * IMGfilter[r][c]

            NewRow.append(abs(Total)) #Why are we doing the absolute value?
        NewIMG.append(NewRow)
        
    return(NewIMG)

def KERNConvolution(Image, IMGfilter, Fun, DxFun):
    NewIMG = []
    BackIMG = []
    FiltLen = len(IMGfilter[0])

    for i in range(0, len(Image[0]) - (FiltLen - 1)):
        NewRow = []
        BackRow = []
        for j in range(0, len(Image[0][0]) - (FiltLen - 1)):
            Total = 0
            for d in range(0,len(IMGfilter)):
                for r in range(0,FiltLen):
                    for c in range(0,FiltLen):
                        Total += Image[d][i+r][j+c] * IMGfilter[d][r][c]

            NewRow.append(Fun(Total)) 
            BackRow.append(DxFun(Total)) 
        NewIMG.append(NewRow)
        BackIMG.append(BackRow)

    return (NewIMG, BackIMG)



def COMBO3D(Images):

    newCon = np.zeros((len(Images[0]), len(Images[0][0]), len(Images[0][0][0]))).tolist()
    for Image in Images:
        newCon = np.array(np.add(Image, newCon)).tolist()
    return newCon

def KERNBACKPNORMAL(Image, IMGfilter, Backp):
    NewIMG = np.zeros((len(Image), len(Image[0]), len(Image[0][0]))).tolist()

    #rint(len(IMGfilter[0][0]))

    FiltLen = len(IMGfilter[0])
    BackInt = 0
    for i in range(0, len(Image[0]) - (FiltLen - 1)):


        for j in range(0, len(Image[0][0]) - (FiltLen - 1)):

            for d in range(0,len(IMGfilter)):
                for r in range(0,FiltLen):
                    for c in range(0,FiltLen):

                        NewIMG[d][i+r][j+c] += IMGfilter[d][r][c] * Backp[BackInt]

            BackInt += 1


    #come back to there is some werid stuff with flattening and stuff and i am worried
    return(NewIMG)


def KERNBACKPConvolution(Image, IMGfilter, Backp):
    #NewIMG = np.zeros((len(IMGfilter),len(IMGfilter[0]),len(IMGfilter[0]))).tolist()
    cubeprop = Chunk(Backp, int(math.sqrt(len(Backp))))

    #print(len(Backp))
    FiltLen = len(cubeprop)

    for d in range(0,len(Image)):

        for i in range(0, len(Image[0]) - (FiltLen - 1)):

            for j in range(0, len(Image[0][0]) - (FiltLen - 1)):

                for r in range(0,FiltLen):
                        for c in range(0,FiltLen):
                            IMGfilter[d][i][j] += Image[d][i+r][j+c] * cubeprop[r][c]


def ConvolutionBackProp(Image, IMGfilter, PrevGradient):

    NewIMG = np.zeros((len(Image),len(Image))).tolist()
    PrevGradInd = 0

    for i in range(0, len(NewIMG)-(len(IMGfilter)-1)):

        for j in range(0, len(NewIMG[0])-(len(IMGfilter)-1)):
            Total = 0

            """            for q in range(len(IMGfilter)):
                        for r in range(3):
                            for c in range(3):
                                NewIMG[i+r][j+c] += IMGfilter[q][r][c] 
            """
            for r in range(len(IMGfilter)):
                for c in range(len(IMGfilter)):
                    NewIMG[i+r][j+c] = IMGfilter[r][c] * PrevGradient[PrevGradInd]


            PrevGradInd += 1



        
    return(NewIMG)

#This is a Neural Network pool
def PoolAry(Kw, Kh, Image):
    NewImage = []

    for i in range(len(Image) - (Kh - 1)):

        NewRow = []

        for j in range(len(Image[0]) - (Kw - 1)):



            #if (i + Kh) <= len(Image) and (j + Kw) <= len(Image[0]):

                max = Image[i][j]

                for r in range(Kh):
                    for c in range(Kw):
                        if Image[i + r][j + c] > max:

                            max = Image[i + r][j + c]

                
                NewRow.append(max)

        NewImage.append(NewRow)

    return NewImage



def SumCheck(x):
    if type(x) != list:
        return x
    return sum(x)

#Turns a 1D list into a 2D list
def Chunk(Lis, Spli):
    newLis = []
    for i in range(0, len(Lis), Spli):
        newLis.append(Lis[i : i + Spli])

    return (newLis)


#Turns a 2D list into a 1D list
def UnChunk(Lis):
    newLis = []
    for i in range(len(Lis)):

        for j in range(len(Lis[i])):

            newLis.append(Lis[i][j])

    return (newLis)

#Turns a 3D list into a 1D list
#I timed the numpy verion and this and
#apperntly looping through the list 
#is faster then numpys reshape
def SuperUnChunk(Lis):
    #size = len(Lis) * len(Lis[0]) * len(Lis[0][0])
    newLis = [] #np.reshape(Lis, (1, size))[0].tolist()
    for i in range(len(Lis)):
        for j in range(len(Lis[i])):
            for k in range(len(Lis[i][j])):
                newLis.append(Lis[i][j][k])
    return newLis

#Divides a list into equal parts
#{CubLis - List} {by - # of list to split into}
def BackpropSplitKern(CubLis, by):
    test = []
    new = int(len(CubLis)/by)
    while(len(CubLis)>0):
        jni = []
        for i in range(new):
            jni.append(CubLis.pop(0))
        test.append(jni)
    return test

def CalcCost(Exp, Real):
    CosList = []
    for i in range(len(Real)):
        CosList.append(2 * (Exp[i] - Real[i]))
    return CosList 


#Cost Activation Function
def RealCalcCost(Exp, Real):
    CosList = []
    for i in range(len(Real)):
        CosList.append(pow(Exp[i] - Real[i], 2))
    return sum(CosList) 


#Finds the Max number in a list
def FindMax(Output):
    Maxam = Output[0]
    Awn = 0
    for i in range(len(Output)):
        if Output[i] > Maxam:
            Maxam = Output[i]
            Awn = i

    return Awn



#Sigmoid Activation Function
def Sigmoid(x):
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0

#Sigmoid Derivative Function
def SigmoidDerv(y):
    return Sigmoid(y) * (1 - Sigmoid(y))


#Tanh Activation Function (this is here so i don't get confused)
def Tanh(x):
    return math.tanh(x)

#Tanh Derivative Function
def TanhDerv(y):
    return 1 - (pow(math.tanh(y), 2))


def CreateKernal(root):
    NewK = np.zeros((root,root)).tolist()
    for i in range(root):
        for j in range(root):
            NewK[i][j] = rand()
    return NewK

#Swish Activation Function
def Swish(x):
    try:
        return x * Sigmoid(x)
    except OverflowError:
        return 0

#Swish Derivative Function
def SwishDerv(y):
    try:
        return y * SigmoidDerv(y) + Sigmoid(y) #Swish(y) + Sigmoid(y) * (1-Swish(y))
    except OverflowError:
        return 0

#Relu Activation Function
def Relu(x):
	return max(0.0, x)

#Relu Derivative Function
def ReluDerv(y):
    return np.greater(y, 0.).astype(np.float32)

#LeakyRelu Activation Function
def LeakyRelu(x):
	return max(x/4, x)

#LeakyRelu Derivative Function
def LeakyReluDerv(y):
    return max(np.sign(y), 0.25)

#Linear Activation Function
def Linear(x):
    return x

#Linear Derivative Function
def LinearDerv(y):
    return 1
    
#Applies Activation Function to a list
def ActivationList(x, Acti):
    newList = []

    for i in x:
        newList.append(Acti(i))
    return newList

#Plutonian initialization method
def Plutonian(n):
    return np.random.uniform(low=-((10*n)/pow(n, 1.85)), high=((10*n)/pow(n, 1.85)))

#He initialization method
def He(n):
    return np.random.normal(loc=0, scale=math.sqrt(2/n))

def rand():
    return random.uniform(-0.35, 0.35)  



#converts a string of float into a list of float
def ConvFloatList(listparam):
    return list(map(float, listparam))

#old Get fresh, keeping it here just incase
"""KrootL = []
for i in Ks:
    for j in i:
        KrootL.append(len(j))
        break

KrootL.reverse()

LayLis = []
for bghjnkl in eferf:
    LayLis.append(bghjnkl)

WFreash = []
for i in range(len(LayLis)):
    l1 = []
    try:

        if(type(LayLis[i+1]) != str):
            for j in range(LayLis[i]):
                l2 = []
                for k in range(LayLis[i + 1]):
                    l2.append(0)
                l1.append(l2)
            WFreash.append(l1)
        else:
            KRint = 0
            addtopool = 2
            ext = 2
            if LayLis[i + 1] != "P":
                ext = 3
                if LayLis[i + 1] == "K":
                    ext = KrootL[KRint]
                    KRint += 1 

            while type(LayLis[i + addtopool]) == str:

                if LayLis[i + addtopool] == "P":
                    ext += 1
                else:
                    if LayLis[i + addtopool] == "K":
                        ext += KrootL[KRint] - 1
                        KRint += 1 
                    else:
                        ext += 2

                addtopool += 1

            for j in range(LayLis[i]):
                l2 = []
                for k in range(int(pow(math.sqrt(LayLis[i + addtopool])-(ext-1), 2))):
                    l2.append(0)
                l1.append(l2)
            WFreash.append(l1)
            while type(LayLis[i + 1]) == str:
                if LayLis[i + 1] == "K":
                    KrootL.pop(0)
                LayLis.pop(i+1)



    except:
        break

return(WFreash)"""

#This creates a Fresh List for Weights
def GetFresh(eferf):
    Fwe = []
    for d2 in eferf:
        Fwe.append(np.zeros((len(d2),len(d2[0]))).tolist())

    return Fwe

#This is used to get text from a file 
class TxtGetW():
    def __init__(self, FileNum):
        NetWeTxt = open("WBL" + str(FileNum) + "/WeightsLay.json", "r")
        Content = json.load(NetWeTxt)
        NetWeTxt.close()
        self.Weights = Content['Weights']
        self.Bias = Content['Bias']

#This gets the Weights from text file
def GetTxT(LayLis):
    WFtxt = []
    WBtxt = []
    RemLis = []

    for ints in LayLis:
        if type(ints) != str:
            RemLis.append(ints)


    for i in range(len(RemLis) - 1):

        FileNum = (len(RemLis) - 2) - i
        FileRead = TxtGetW(FileNum)
    
        FileWeights = FileRead.Weights
        FileBias = FileRead.Bias

        WFtxt.append(FileWeights)
        WBtxt.append(FileBias)

    return((WFtxt, WBtxt))


#Creates Weights in a text file, 
#All of this code is bad but does not need to be good 
#it just needs to work Because it's only triggered once
def MakeTxT(Frame):
    LayLis = Frame.NeurList
    CopyLis = []
    WFreash = []
    Oglen = len(LayLis)
    Kerns = []
    BlankKerns = []

    for ints in LayLis:
        if type(ints) == str:
            Oglen -= 1
        CopyLis.append(ints)

    KernInt = 0
    DepthList = []
    KrootL = []



    #for nhjik in Frame.Kernals:
    for s in range(len(LayLis)):
        if(LayLis[s] == "K"):
            Dtc = 1
            if(LayLis[s+1] == "K"):
                Dtc = Frame.Kernals[KernInt+1][0]



            BDKern = []
            TDKern = [] 
            for kr in range(Frame.Kernals[KernInt][0]):
                TDKern.append([])
                BDKern.append([])
                for d in range(Dtc):
                    TDKern[kr].append(CreateKernal(Frame.Kernals[KernInt][1]))
                    BDKern[kr].append(np.zeros((Frame.Kernals[KernInt][1], Frame.Kernals[KernInt][1])).tolist())
                    
            Kerns.append(TDKern)
            BlankKerns.append(BDKern)
            DepthList.append(Frame.Kernals[KernInt][0]) #making depth
            KrootL.append(Frame.Kernals[KernInt][1])
            KernInt += 1   
            KernDone = True 

    Kdt = 1
    for i in range(len(LayLis) - 1):
    #while (i < len(LayLis) - 1):
        
        FileNum = (Oglen - 2) - i

        if FileNum > -1:

            if type(LayLis[i+1]) == str:
                srtTofile = []
                KernDone = False
                for j in range(LayLis[i]):

                    if type(LayLis[i+1]) == str:
                        SetKP = False
                        KRint = 0
                        #Kdt = 1
                        srtTofile.append([])
                        addtopool = 2
                        ext = 2
                        #print(KRint)
                        if LayLis[i + 1] != "P":
                            SetKP = True
                            Kdt = DepthList[KRint]
                            ext = 3

                            if LayLis[i + 1] == "K":
                                ext = KrootL[KRint]
                                KRint += 1 

                        while type(LayLis[i + addtopool]) == str:
                            

                            if LayLis[i + addtopool] == "P":
                                ext += 1
 
                            else:
                                if LayLis[i + addtopool] == "K":
                                    if not SetKP:
                                        Kdt = DepthList[KRint]
                                        SetKP = True
                                    ext += KrootL[KRint] - 1
                                    KRint += 1 
                                else:
                                    ext += 2

                            addtopool += 1


                        MakeThis = int(pow(math.sqrt(LayLis[i + addtopool])-(ext-1), 2)) * Kdt

                        for k in range(MakeThis):

                            srtTofile[j].append(Plutonian(MakeThis))#np.random.normal(loc=0, scale=math.sqrt(2/int(pow(math.sqrt(LayLis[i + addtopool])-(addtopool-1), 2)))))

                while type(LayLis[i + 1]) == str:
                    if LayLis[i + 1] == "K":
                        KrootL.pop(0)
                        DepthList.pop(0)
                    
                    LayLis.pop(i+1)
                    
            else:
                srtTofile = []
                for j in range(LayLis[i]):
                    srtTofile.append([])
                    for k in range(LayLis[i + 1]):

                        srtTofile[j].append(Plutonian(LayLis[i + 1]))#np.random.normal(loc=0, scale=math.sqrt(2/LayLis[i + 1])))


            NewData = json.loads('{"Weights": [], "Bias":0}')
            NewData['Weights'] = srtTofile
            OpenFile = open("WBL" + str(FileNum) + "/WeightsLay.json", "w")
            json.dump(NewData, OpenFile)
            OpenFile.close()
            


    Kerns.reverse()
    BlankKerns.reverse()

    SavedFrame = json.loads('{"Neurons": 0, "Activtions": 0, "CostFunction":0 , "Pooling":0, "Chunk":0, "LoadingBar":0, "Filters":0, "FiltFun":0}')
    SavedFrame['Neurons'] = CopyLis
    SavedFrame['Activtions'] = Frame.ActivName
    SavedFrame['CostFunction'] = Frame.CostFun.__name__
    SavedFrame['Pooling'] = Frame.PoolNumb
    SavedFrame['Chunk'] = Frame.ChunkNumb
    SavedFrame['LoadingBar'] = Frame.loadbar.__name__
    SavedFrame['Filters'] = str(Frame.Filters)
    if(type(Frame.KernalFun) != list):
        SavedFrame['FiltFun'] =  (Frame.KernalFun)
    else:
        SavedFrame['FiltFun'] = "[]"

    OpenFile = open("NetworkInfo.json", "w")
    json.dump(SavedFrame, OpenFile)
    OpenFile.close()

    KernalFrame = json.loads( '{"Kernals":0 }')
    KernalFrame['Kernals'] = str(Kerns)
    OpenKFile = open("Kernals/AllKernals.json", "w")
    json.dump(KernalFrame, OpenKFile)
    OpenFile.close()

    KernalFrame = json.loads( '{"Kernals":0 }')
    KernalFrame['Kernals'] = str(BlankKerns)
    OpenKFile = open("Kernals/BlankKerns.json", "w")
    json.dump(KernalFrame, OpenKFile)
    OpenFile.close()
    
    print("Previous data overwritten, New data inserted")
    return(WFreash)


#Adds to Weights in the text file 
def AddTxT(NewLis, OldLays, DevBy):
    WeiLis = NewLis[0]
    BiaLis = NewLis[1]
    OldWei = OldLays[0]
    OldBia = OldLays[1]

    NewWei = []
    NewBia = []
    for i in range(len(WeiLis)):

        srtTofile = []
        biaTofile = (OldBia[i] + (BiaLis[i] / DevBy))
        FileNum = (len(WeiLis) - 1) - i

        for j in range(len(WeiLis[i])):
            srtTofile.append([])
            for k in range(len(WeiLis[i][j])):
                srtTofile[j].append(OldWei[i][j][k] + (WeiLis[i][j][k] / DevBy))


        NewData = json.loads('{"Weights": [], "Bias":0}')
        NewData['Weights'] = srtTofile
        NewData['Bias'] = biaTofile
        OpenFile = open("WBL" + str(FileNum) + "/WeightsLay.json", "w")
        json.dump(NewData, OpenFile)
        OpenFile.close()


        NewWei.append(srtTofile)
        NewBia.append(biaTofile)


    return (NewWei, NewBia)

#this gets the Bias from text file
def GetBia(LayLis):
    Biatxt = []

    for i in range(len(LayLis) - 1):

        FileNum = (len(LayLis) - 2) - i
        Data = open("WBL" + str(FileNum) + "/BiasLay.txt", "r")
        Content = Data.read()
        Data.close()

        Biatxt.append(float(Content))

    return(Biatxt)


#Adds to Bias in the text file 
def AddBia(BiaLis, OGLay, DevBy):
    OGBia = GetBia(OGLay)
    for i in range(len(BiaLis)):

        srtTofile = ""
        FileNum = (len(BiaLis) - 1) - i

        srtTofile += str(OGBia[i] + (BiaLis[i] / DevBy))


        open("WBL" + str(FileNum) + "/BiasLay.txt", "w").write(srtTofile)

#This creates a Fresh List for Bias
def FreshBi(BiLa):
    fre = []
    for i in range(len(BiLa)):
        fre.append(0)
    
    return(fre)

#Calculation foe example 
def CalcExpe(x):
    NEl = []
    for i in range(10):

        if i == x:

            NEl.append(1)

        else:

            NEl.append(0)
        
    return NEl



DerivativeDic = { 
                    Sigmoid : SigmoidDerv,
                    Tanh : TanhDerv,
                    Swish : SwishDerv,
                    Linear : LinearDerv,
                    Relu : ReluDerv,
                    LeakyRelu : LeakyReluDerv
                }


#these are just loading functions


def LoadingBarPre(LoadingPro):
    LoadingPro += "█"
    LoadUn = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░⦘"
    sys.stdout.write("\033[F")
    NewLoad = "⦗" + LoadingPro + LoadUn[len(LoadingPro) : 51]
    print(NewLoad)


    return LoadingPro


def LoadingBarHig(LoadingPro):
    LoadingPro += "▩"
    LoadUn = "□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□⦘"
    sys.stdout.write("\033[F")
    NewLoad = "⦗" + LoadingPro + "█" + LoadUn[len(LoadingPro) : 51]
     
    print(NewLoad)
    if NewLoad == "⦗▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩█⦘":
        sys.stdout.write("\033[F")
        print("⦗▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩⦘")
        print("\n")
        return ""

    return LoadingPro



def LoadingText(LoadingPro):
    LoadingDic = {
                     "│" : "╱", 
                     "╱" : "──",
                    "──" : '╲ ',
                    '╲ ' : '│',
                      "" : '│',
                 }
    LoadingPro = LoadingDic[LoadingPro]
    sys.stdout.write("\033[F")
    print("Loading: " + LoadingPro)
    return LoadingPro


def LoadingCir(LoadingPro):
    LoadingDic = {
                     "◜ " : " ◝", 
                     " ◝" : " ◞",
                    " ◞" : '◟ ',
                    '◟ ' : '◜ ',
                      "" : '◜ ',
                 }
    LoadingPro = LoadingDic[LoadingPro]
    sys.stdout.write("\033[F")
    print("Loading: " + LoadingPro)
    return LoadingPro


def LoadingCirFull(LoadingPro):
    LoadingDic = {
                     "◴" : "◷", 
                     "◷" : "◶",
                     "◶" : "◵",
                     "◵" : "◴",
                      "" : '◴',
                 }
    LoadingPro = LoadingDic[LoadingPro]
    sys.stdout.write("\033[F")
    print("Loading: " + LoadingPro)
    return LoadingPro




def LoadingCard(LoadingPro):

    if LoadingPro == ""  or int(LoadingPro[0:6]) > 127150:
        LoadingPro = "127137"

    CardInt = int(LoadingPro[0:6])  

    LoadingPro += chr(CardInt)

    sys.stdout.write("\033[F")
    
    AfterNumb = LoadingPro[6 : len(LoadingPro)]

    print("Loading: " + AfterNumb + "🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘"[len(LoadingPro) - 6: 14])

    LoadingPro = str(CardInt + 1) + AfterNumb 


    return LoadingPro


def LoadingDice(LoadingPro):

    if LoadingPro == ""  or int(LoadingPro[0:4]) > 9861:
        LoadingPro = "9856"

    CardInt = int(LoadingPro[0:4])  

    LoadingPro = str(CardInt + 1) + chr(CardInt)

    sys.stdout.write("\033[F")
    

    print("Loading: " + LoadingPro[4:5])



    return LoadingPro