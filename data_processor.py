import json
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from matplotlib import pylab

def extract_hash_tags(s):
    '''
    This function takes a tweet as input and extracts the hashtags.     
    '''
    ret = list(set(part[1:] for part in s.split() if part.startswith('#')))
    ret = [x[:-1] if x.endswith('.') or x.endswith(',') else x for x in ret]
    ret = [x.lower() for x in ret]
    ret = [x.encode('ascii', 'ignore') for x in ret]
    return ret

def draw_graph(G, file_name):
    '''
    This function takes the graph created using networkx and the file
    name as input and draws the graph. 
    '''
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(G) 
    edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
    
    nx.draw_networkx_nodes(G,pos)
    nx.draw(G, pos, edgelist=edges, node_size=[v * 100 for v in d.values()], edge_color=weights, width=2.0, edge_cmap=plt.cm.Reds)
    nx.draw_networkx_labels(G,pos)
    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

def make_graph(n):
    '''
    This function takes a keyword as input and will extract the data
    from the corresponding json file. It will then make a weighted graph 
    using Networkx. The graph is weighted depending on the number of times
    it is in the same tweet as another hashtag. It then saves the graph in 
    pdf form.
    '''
    hashtags = []
    fname = n + '.json'
    i = 0
    with open(fname) as f:
        for line in f:
            # This is the limit for number of tweets - change it as needed
            if i == 800:
                break
            i += 1
            tweet = json.loads(line)
            text = tweet['text']
            h = extract_hash_tags(text)
            if h != []:
                hashtags.append(h)
    
    G=nx.Graph(name=n + '_graph')
    for hs in hashtags:
        comb = list(itertools.combinations(hs, 2))
        for a, b in comb:
            if G.has_edge(a, b):
                G[a][b]['weight'] += 1.0
            else:
                G.add_edge(a, b, weight=1.0)
    # This is a cutoff for minimum degree in the top graph - change it as needed          
    cutoff = 5
    # This makes a graph with only edges that meet the cutoff
    top = [edge for edge in G.edges_iter(data=True) 
           if edge[2]['weight'] > cutoff]
    G2 = nx.MultiGraph(top)
    gnametop = n + '_graph_top.pdf'
    draw_graph(G2, gnametop)
        
    return G, i
                
if __name__ == "__main__":     
    # This is the keyword to name your graphs - change it as needed
    n = 'royal'
    G, i = make_graph(n)
    
    d = nx.degree(G)
    gname = n + '_graph.pdf'
    draw_graph(G, gname)
    print nx.info(G)
    print "Average clustering: ", nx.average_clustering(G)
    print "Tweets iterated: ", i
   
