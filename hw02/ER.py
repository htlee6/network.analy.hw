__author__ = 'htlee'
__email__ = 'hauten.lee@mail.bnu.edu.cn'

import networkx as nx
import matplotlib.pyplot as plt
import random
import collections
import csv
import os

n = 10  # number of nodes
p = 0.4  # prob to connection between any pair of nodes

options = {
    'node_color': 'black',
    'node_size': 100,
    'width': 3
}


def write2files(n, p, deg, deg_dist, cluster_coef, betweenness):

    # TODO the structure of file is to be organized

    def properly_numbered_filename(fn):
        i = 0
        _maybepath = fn
        while os.path.isfile(_maybepath+"_"+str(i)+'.csv'):
            i = i + 1
        return fn + '_' + str(i)

    dicts = deg, deg_dist, cluster_coef, betweenness
    filename = 'n_' + str(n) + "_p_" + str(p)
    filename = properly_numbered_filename(filename)
    # write in the same parent directory
    filename = "./" + filename + ".csv"
    with open(filename, 'w') as opfile:
        field_names = ['id', 'deg', 'deg_dist', 'cluster_coef', 'betweenness']
        writer = csv.writer(opfile, delimiter=',')
        writer.writerow(field_names)
        for key in deg:
            writer.writerow([key] + [d[key]] for d in dicts)


def norm2distribution(deg_stat):
    s = 0
    res = {}
    for i in deg_stat:
        s = s + deg_stat[i]
    for i in deg_stat:
        res[i] = deg_stat[i] / s
    return res


class Graph(nx.Graph):
    def degree_distribution(self, plot=True, subplot=False):
        degree_sequence = sorted([d for n, d in self.degree()], reverse=True)  # degree sequence
        degree_stat = collections.Counter(degree_sequence)

        reversed_degree_sequence = sorted([d for n, d in self.degree()], reverse=False)
        reversed_degree_stat = collections.Counter(reversed_degree_sequence)
        normalized_distribution = norm2distribution(reversed_degree_stat)

        deg, cnt = zip(*degree_stat.items())

        if plot is True:
            if subplot is True:
                fig, ax = plt.subplots()
                plt.bar(deg, cnt, width=0.80, color="b")

                plt.title("Degree Histogram")
                plt.ylabel("Count")
                plt.xlabel("Degree")
                ax.set_xticks([d + 0.4 for d in deg])
                ax.set_xticklabels(deg)

                # draw graph in inset
                plt.axes([0.4, 0.4, 0.5, 0.5])
                Gcc = self.subgraph(sorted(nx.connected_components(self), key=len, reverse=True)[0])
                pos = nx.spring_layout(self)
                plt.axis("off")
                nx.draw_networkx_nodes(self, pos, node_size=20)
                nx.draw_networkx_edges(self, pos, alpha=0.4)
            else:
                _, ax = plt.subplots()
                plt.bar(deg, cnt, width=0.80, color="b")

                plt.title("Degree Histogram")
                plt.ylabel("Count")
                plt.xlabel("Degree")
                ax.set_xticks([d + 0.4 for d in deg])
                ax.set_xticklabels(deg)
            plt.show()

        return dict(degree_stat), normalized_distribution


def simulate_ER(n, p):
    # initiate a graph
    g = Graph()

    # initiate n nodes
    for i in range(n):
        g.add_node(i)

    # consider every possible pair of nodes pair(x,y), if they will be connected
    for x in range(0, n):
        for y in range(x, n):
            random_val = random.random()
            if random_val <= p and x != y:  # connect!
                g.add_edge(x, y)
    return g


if __name__ == '__main__':
    g = simulate_ER(n=n, p=p)
    # Visualize the graph g
    nx.draw(g, pos=nx.circular_layout(g), with_labels=True)
    plt.show()
    deg, deg_dist = g.degree_distribution(plot=False, subplot=False)
    cluster_coef = nx.clustering(g)
    betweenness = nx.algorithms.centrality.betweenness_centrality(g, normalized=False)

    print('degree:', deg, '\n', 'degree distribution:', deg_dist, '\n', 'clustering coefficient:', cluster_coef, '\n', 'betweenness:', betweenness, '\n')

    # Write data to file
    # write2files(n, p, deg, deg_dist, cluster_coef, betweenness)
