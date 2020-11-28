__author__ = 'htlee'
__email__ = 'hauten.lee@mail.bnu.edu.cn'

import networkx as nx
import collections
import random
import matplotlib.pyplot as plt

# N >> K >> lnN >> 1
N = 40  # number of nodes
K = 10  # the mean node (assumed to be an even number)
Beta = 0.5  # rewire probability, special param, 0 <= Beta <= 1


class Graph(nx.Graph):
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


def simulate_WS(n, k, beta):
    # initiate a graph
    g = Graph()

    # initiate n nodes
    for i in range(n):
        g.add_node(i)

    def plus_1(curpos, ringlength):
        if curpos == ringlength - 1:
            return 0
        return curpos + 1

    def minus_1(curpos, ringlength):
        if curpos == 0:
            return ringlength - 1
        return curpos - 1

    # connect k-nearest neighbors
    for i in range(0, n):
        left = minus_1(i, n)
        right = plus_1(i, n)
        for iters in range(int(k/2)):
            g.add_edge(left, i)
            g.add_edge(right, i)
            left = minus_1(left, n)
            right = plus_1(right, n)

    # rewire randomly
    for i in range(0, n):
        # iterate through i-th node's K/2 rightmost neighbors
        right = plus_1(i, n)
        for iters in range(int(k/2)):
            print(i, iters, right)
            # if rewire? the random value calls
            p = random.random()
            if p <= Beta:
                # break the link
                g.remove_edge(i, right)
                # rewire uniformly, avoiding self-loop and existing links
                candidates = list()
                for v in range(0, n):
                    if not g.has_edge(v, i) and v != i and v != right:
                        candidates.append(v)
                winner = random.choice(candidates)
                g.add_edge(i, winner)

            right = plus_1(right, n)  # general update

    return g


if __name__ == '__main__':
    g = simulate_WS(n=N, k=K, beta=Beta)
    nx.draw(g, pos=nx.circular_layout(g), with_labels=True)
    plt.show()
    cluster_coef = nx.clustering(g)
    print(cluster_coef)