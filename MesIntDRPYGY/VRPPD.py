
import time
import random
import math
#import fg
import numpy as np

def datagen(citySize, seed,min,max):
    items = []
    citys = {}
    random.seed(seed)
    for i in range(citySize):
        z = random.randint(min,max)
        k = random.randint(min,max)
        a = (z , k)
        citys[i] = {
             "start" : a,
            "end" : a 
        }
    return citys
    

def manhAbs(c1,c2):
    return abs((c1[0] - c2[0])) + abs((c1[1] - c2[1]))


def calcRouteLenght(citysList: dict, sorozat: list, startLoc,startList: list, available: list,listStart):
    distance = math.inf
    smallest = 0
    #print(available)
    if len(startList) == 0:
        startList.append(startLoc)
    for i in range(len(available)):
        a = available[i]
        #print(a)
        testDist = manhAbs(startList[listStart],citysList[a]["start"]) 
        if testDist < distance :
            distance = testDist
            #print(distance, " csere volt")
            smallest = i
    sorozat.append(available[smallest])
    listStart = listStart + 1
    startList.append(citysList[smallest]["end"])
    available.remove(available[smallest])
    #print(startList)
    if len(available) > 0:
       eredmeny = (calcRouteLenght(citysList,sorozat,startList[listStart],startList,available,listStart))
    else:
        sorozat.append(-1)
    return sorozat

#EZT MEG KELL CSINÁLNI
def improvedSearching(cityList: dict,keys: list ,iteration, startPoint):
    tabuList = []
    
    b_dist = calcIterLenght(cityList,keys,startPoint)
    b_order = keys.copy()
    random.seed(363212)
    for i in range(iteration):
        a = random.randint(0,(len(keys)-1))
        b = random.randint(0,(len(keys)-1))
        keys[a] , keys[b] = keys[b] , keys[a]
        c_dist = calcIterLenght(cityList,keys,startPoint)
        #print("or: ",b_order)
        #print("key: ", keys)
        #print(c_dist)
        if c_dist < b_dist :
            b_dist = c_dist
            b_order = keys.copy()
            
        
    print(b_dist)
    return b_order

def calcIterLenght(cityList: dict, keyList: list, StartPoint):
    lenght = 0
    lenght += manhAbs(StartPoint,cityList[keyList[0]]["start"])
    for i in range(len(keyList)-1):
        lenght += manhAbs(cityList[keyList[i]]["end"],cityList[keyList[i+1]]["start"])
    lenght += manhAbs(cityList[keyList[len(keyList)-1]]["end"],StartPoint)
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
                #a = random.randint(0,len(available))
                #b = random.randint(0,len(available))
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

def setEndPointPairs(cityList: dict, duoList: list):
    newCityList = cityList.copy()
    for i in range(len(duoList)):
        newCityList[duoList[i][0]]["end"] = cityList[duoList[i][1]]["start"]
        #print(cityList[duoList[i][0]]["end"])
        #print(newCityList[duoList[i][0]]["end"])
    return newCityList


def findAllCourierRoute(citylist: dict, duos: list ,courier: list, startPoint, rep,tabuSize: int):
    random.seed(34121012)
    tabu = []
    routeNum = len(courier)
    routeBests = []
    bestOverAll = 0
    for i in range(routeNum):
        a, b = improvedSearching2(citylist,courier[i],duos,80,startPoint, tabuSize)
        bestOverAll += a
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
            recordAttempt = 0
            RbList = []
            for i in range(routeNum):
                rA, Rb = improvedSearching2(citylist,courier[i],duos,50,startPoint, tabuSize)
                recordAttempt += rA
                RbList.append(Rb)
            if recordAttempt < bestOverAll : 
                bestOverAll = recordAttempt
                routeBests= RbList.copy()
                print("new BEST", recordAttempt , RbList)
    print(routeBests)
    return bestOverAll


def improvedSearching2(cityList: dict,keys: list ,duos: list,iteration, startPoint, tabuMaxSize: int):
    tabuList = []
    duoS = []
    duoE = []
    iteration = iteration * int(len(keys)*(2.9))
    for j in range(len(duos)):
        a = duos[j][0]
        if keys.count(a) > 0 :
            duoS.append(duos[j][0])
            duoE.append(duos[j][1])

    f_order = keys.copy() + duoE

    b_dist = calcIterLenght(cityList,f_order,startPoint)
    b_order = f_order.copy()

    f_oredCopy = f_order.copy()
    #beszúrom a duo hátsó tagjait az első tagok mögé mert úgy is mindig páros lesz
    duoS = duoS + duoE
    
    #TESZTÜZEM
    '''
    print(duoS)
    teszt = duoS.index(7)
    if teszt < len(duoS)/2:
        print("Elso szam")
        print(duoS[int(teszt + len(duoS)/2)])
    else:
        print("Masodik szam")
        print(duoS[int(teszt - len(duoS)/2)])
    '''
    #TESZTÜZEM

    #random.seed(386512)
    
    for i in range(iteration):
        #a = random.randint(0,(len(f_order)-1))
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
        
    #print(b_dist, " sorrend " , b_order, " tabulista ", tabuList)
    
    return b_dist , b_order




def main():
    # általában tesztelt seed (5,2,0,20)
    
    bad = datagen(10,2,0,20)
    print(bad)
    
    duos = generateDuos(list(bad.keys()),2)
    print("duos: ", duos)
    goodNums = availablePoints(duos,list(bad.keys()))
    print("available: ", goodNums)
    vart = splitForDelivery(goodNums,2)
    print("futarok: ",vart)
    print(findAllCourierRoute(bad, duos, vart, (10,10),7000,10))
    #müködö
    #solution = improvedSearching(bad,1000000,(10,10))
    #print("Solution: ",solution)
    #müködö
    #print(calcIterLenght(bad,[3,4,2,1,0],(10,10)))
    #utvonal= calcRouteLenght(bad,[],(10,10),[],list(bad.keys()),0)
    #print("elso:" ,utvonal)
    #fg.helpGraph(bad)
main()