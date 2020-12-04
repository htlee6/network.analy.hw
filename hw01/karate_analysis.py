import networkx as nx
import matplotlib.pyplot as plt
import collections
import csv


def savecsv(dict, path):
    with open(path, 'w') as file:
        writer = csv.writer(file)
        for key, value in dict.items():
            writer.writerow([key, value])


class Graph(nx.Graph):
    def __init__(self, G):
        super(nx.Graph, self).__init__(G)

    def degree_distribution(self, plot=True, subplot=False):

        def norm2distribution(deg_stat):
            s = 0
            res = {}
            for i in deg_stat:
                s = s + deg_stat[i]
            for i in deg_stat:
                res[i] = deg_stat[i] / s
            return res

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


if __name__ == '__main__':
    with open('karate.txt', 'r') as karate_data:
        G = nx.read_edgelist(karate_data)

    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    cnt_sum = sum(cnt)
    norm_cnt = []
    for i in range(len(cnt)):
        norm_cnt.append(cnt[i]/cnt_sum)

    # ******** DEGREE DISTRIBUTION ******** #
    # Canvas Configuration
    plt.figure(figsize=(12, 9))

    fig, ax = plt.subplots()
    plt.bar(deg, norm_cnt, width=0.80, color="b")

    plt.title("Degree Distribution in Karate Club Network")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    pos = nx.spring_layout(G)
    plt.axis("off")
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    plt.savefig("degree_dist.svg")

    # ********* CLUSTERING COEFFICIENT ********** #
    cluster_coef = nx.clustering(G)

    # ********* BETWEENNESS ********** #
    betweenness = nx.algorithms.centrality.betweenness_centrality(G, normalized=False)

    print("clustering coef:", cluster_coef)
    savecsv(cluster_coef, path="clustering.csv")
    print("! Saved to file")
    print("betweenness:", betweenness)
    savecsv(betweenness, path='betweenness.csv')
    print("! Saved to file")

    pass