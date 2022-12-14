import time
import random
import math
import numpy as np

def datagen(citySize, seed,min,max):
    citys = {}
    random.seed(seed)
    i = 0
    while i < citySize:
        z = random.randint(min,max)
        k = random.randint(min,max)
        a = (z , k)
        if a not in citys:
            citys[i] = {
             "coord" : a
            }
            i += 1

    return citys


def manhAbs(c1,c2):
    return abs((c1[0] - c2[0])) + abs((c1[1] - c2[1]))


def calcIterLenght(cityList: dict, keyList: list, StartPoint):
    lenght = 0
    lenght += manhAbs(StartPoint,cityList[keyList[0]]["coord"])
    for i in range(len(keyList)-1):
        lenght += manhAbs(cityList[keyList[i]]["coord"],cityList[keyList[i+1]]["coord"])
    lenght += manhAbs(cityList[keyList[len(keyList)-1]]["coord"],StartPoint)
    return lenght


def splitForDelivery(keyList: list, courier):
    arr = []
    rows = courier
    for i in range(rows):
        col=[]
        for j in range(len(keyList)):
            if j % courier == i :
                col.append(keyList[j])
        arr.append(col)
    return arr

def generateDuos(keyList: list, db):
    pairList = []
    if len(keyList)/2+1 > db : 
        available = keyList.copy()
        for i in range(db):
            pair = []
            a = 0
            b = 0
            while a == b :
                a = random.choice(available)
                b = random.choice(available)
            pair.append(a)
            pair.append(b)
            pairList.append(pair)
            available.remove(a)
            available.remove(b)
    return pairList

def availablePoints(pairlist: list, keyList: list):
    keys = keyList.copy()
    for i in range(len(pairlist)):
        keys.remove(pairlist[i][1])
    return keys


def findAllCourierRoute(citylist: dict, duos: list ,courier: list, startPoint, rep,tabuSize: int):
    random.seed(420)
    bestLeghts = []
    routeNum = len(courier)
    routeBests = []
    bestOverAll = 0

    for i in range(routeNum):
        a, b = improvedSearching2(citylist,courier[i],duos,rep,startPoint, tabuSize)
        bestOverAll += a
        bestLeghts.append(a)
        routeBests.append(b)
    if routeNum > 1 :
        #print("Csak a legjobbak: ",routeBests , bestOverAll)
        for i in range(rep) :
            good = 0
            while good == 0 :
                a = random.randint(0,routeNum-1) 
                if len(courier[a]) > 2 :
                    good = 1
            b = random.choice(courier[a])
            courier[a].remove(b)
            target = a
            while target == a:
                target = courier.index(random.choice(courier)) 
            courier[target].append(b)
            
            rAList = []
            recordAttempt = 0
            RbList = []
            for i in range(routeNum):
                rA, Rb = improvedSearching2(citylist,courier[i],duos,50,startPoint, tabuSize)
                recordAttempt += rA
                rAList.append(rA)
                RbList.append(Rb)
            if recordAttempt < bestOverAll : 
                bestOverAll = recordAttempt
                routeBests= RbList.copy()
                bestLeghts= rAList.copy()
                #print("new BEST", recordAttempt , RbList)
    #print(routeBests, bestLeghts)
    return bestOverAll , routeBests , bestLeghts


def improvedSearching2(cityList: dict,keys: list ,duos: list,iteration, startPoint, tabuMaxSize: int):
    random.seed(420)
    tabuList = []
    duoS = []
    duoE = []
    iteration = iteration * int(len(keys)*(1.6))
    for j in range(len(duos)):
        a = duos[j][0]
        if keys.count(a) > 0 :
            duoS.append(duos[j][0])
            duoE.append(duos[j][1])

    f_order = keys.copy() + duoE

    b_dist = calcIterLenght(cityList,f_order,startPoint)
    b_order = f_order.copy()

    f_oredCopy = f_order.copy()
    #besz??rom a duo h??ts?? tagjait az els?? tagok m??g?? mert ??gy is mindig p??ros lesz
    duoS = duoS + duoE


    for i in range(iteration):
        flasback = f_oredCopy.copy()
        a = random.randint(1,len(f_oredCopy)-1)
        aV = f_oredCopy[a]
        if duoS.count(aV) > 0 :
            teszt = duoS.index(aV)
            if teszt > len(duoS)/2:
                #print("e",f_oredCopy,"av:",aV)
                f_oredCopy.remove(aV)
                #print("e",f_oredCopy,"av:",aV)
                tg = f_oredCopy.index(duoS[int(teszt - len(duoS)/2)])
                #print(" tg: ",tg , f_oredCopy[tg])

                f_oredCopy.insert(tg+1,aV)
        else:
            f_oredCopy.remove(aV)
            f_oredCopy.insert(0,aV)

        #print("h",f_oredCopy)
        if tabuList.count(f_oredCopy) == 0 :
            #print("yee")
            c_dist = calcIterLenght(cityList,f_oredCopy,startPoint)
            if c_dist < b_dist :
                b_dist = c_dist
                b_order = f_oredCopy.copy()
            tabuList.append(f_oredCopy.copy())
            if len(tabuList) > tabuMaxSize :
                tabuList.pop(0)
        else:
            f_oredCopy = flasback

    #print(b_dist, " sorrend " , b_order, " tabulista ", tabuList)

    return b_dist , b_order

def VRPPDCalc(randomCitys,numberOfCourier,numberOfTabu,numberOfPair,cycle,StartPoint):

    duos = generateDuos(list(randomCitys.keys()),numberOfPair)

    pickableCityes = availablePoints(duos,list(randomCitys.keys()))

    Couriers = splitForDelivery(pickableCityes,numberOfCourier)
    
    return findAllCourierRoute(randomCitys, duos, Couriers, StartPoint, cycle,numberOfTabu)
