import matplotlib.pyplot as plt

def helpGraph(data: dict):
    plt.rcParams["figure.figsize"] = [8, 5]
    plt.rcParams["figure.autolayout"] = True
    trans = list(data.values())
    solution = list(data.keys())

    for i in range(len(solution)):
        #plt.plot(bad[solution[i]]["start"][0], bad[solution[i]]["start"][1], 'o-r')
        #plt.plot(solution,'o-r')
        plt.plot(trans[i]["start"][0],trans[i]["start"][1],'o-r')
    
    plt.axis([0, 20, 0, 20])


    plt.show()

    return 0