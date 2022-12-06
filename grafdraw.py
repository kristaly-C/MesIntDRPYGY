import networkx as nx
import matplotlib.pyplot as plt

def printableFormatter(cityList: dict, routeList: list):
    for i in range(len(routeList)):
        routeList[i].insert(0,'S')
        routeList[i].append("S")
    return routeList



def graphDraw(cityCors: dict, listOfRoutes: list,startPoint):
    plt.rcParams["figure.figsize"] = [8, 5]
    plt.rcParams["figure.autolayout"] = True

    listOfRoutes = printableFormatter(cityCors, listOfRoutes)

    g = nx.DiGraph()
    ckey = list(cityCors.keys())
    cval = list(cityCors.values())
    #print(cval[0]["start"])
    g.add_node("S",pos=startPoint)
    for i in range(len(cityCors.keys())):
        g.add_node(ckey[i],pos=cval[i]["coord"])
    
    colorList = ["gold", "red", "violet", "pink", "limegreen",
              "blue", "darkorange","skyblue","black"]
    for j in range(len(listOfRoutes)):
        for i in range(len(listOfRoutes[j])-1) :
            g.add_edge(listOfRoutes[j][i],listOfRoutes[j][i+1], color=colorList[j])
    
    pos=nx.get_node_attributes(g,'pos')
    edges = g.edges()
    colors = [g[u][v]['color'] for u,v in edges]
    nx.draw(g,pos,arrows=True, with_labels = True,edge_color=colors, node_color='skyblue', node_size=250, width=2.5)
    plt.show()

