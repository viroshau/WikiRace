import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from getLinksFromPageWikipedia import Page, getAllLinksOnPageInitialVersion

PAGENAME = 'Alons'
WIKIBASEURL = 'https://en.wikipedia.org'
PAGEURL = WIKIBASEURL + '/wiki/' + PAGENAME

COLORS = ['#264653','#2a9d8f','#e9c46a','#f4a261','#e76f51']

def plotAllOutGoingGraphsWithName(url):
    startPage = Page(PAGENAME, PAGEURL, None, history=[PAGENAME])
    linksOnFirstPage = getAllLinksOnPageInitialVersion(url)
    G = nx.Graph()
    colorMap = []
    colorMap.append(COLORS[0])
    for link in linksOnFirstPage:
        G.add_edge(PAGENAME, link)
        colorMap.append(COLORS[1])
    nx.draw(G,with_labels = True,node_color = colorMap)
    plt.show()

def plotGraphWithVaryingNodeSizes(url):
    #Use the 'Alons' pageName for a nice graphic. Does not have too many outgoing links. 
    linksOnFirstPage = getAllLinksOnPageInitialVersion(url)
    G = nx.Graph()
    nodecolors = {}
    #nodecolors[PAGENAME] = COLORS[0]
    nodecolors.setdefault(PAGENAME,COLORS[0])
    for link in linksOnFirstPage:
        nodecolors.setdefault(link,COLORS[1])
        G.add_edge(PAGENAME,link)
        outgoingLinksFromThisLink = getAllLinksOnPageInitialVersion(linksOnFirstPage[link])
        for subLink in outgoingLinksFromThisLink:
            nodecolors.setdefault(subLink,COLORS[2])
            G.add_edge(link,subLink)
    nodeSizes = []
    for node in G.nodes():
        nodeSizes.append(len(G.edges(node)))
    nx.draw(G,with_labels = True,node_size = np.array(nodeSizes)*100,node_color = nodecolors.values(),edge_color= 'lightgray')
    plt.show()

plotGraphWithVaryingNodeSizes(PAGEURL)

