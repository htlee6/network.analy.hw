import networkx as nx
import matplotlib.pyplot as plt

with open('karate.txt', 'r') as karate_data:
    g = nx.read_edgelist(karate_data)


# Canvas Configuration
plt.figure(figsize=(12, 12))
plt.title('Visualization of Karate Club Network')

nx.draw(g, with_labels=False)
# plt.show()
plt.savefig('karate_viz.pdf')
