from travelling_salesman import problem_solution
import matplotlib.pyplot as plt
import networkx as nx
import random
import string
import numpy as np

random.seed(11)
np.random.seed(121)
INDIVIDUAL_SIZE = NUMBER_OF_CITIES = 5
POPULATION_SIZE = 20
N_ITERATIONS = 100
N_MATINGS = 10

cities = [
    ''.join(
        np.random.choice(
            [ c for c in string.ascii_letters ], random.randint(5, 12)
        )
    ) for i in range(NUMBER_OF_CITIES)
]

distances = np.zeros((NUMBER_OF_CITIES, NUMBER_OF_CITIES))

for city in range(NUMBER_OF_CITIES):
    for to_city in [i for i in range(NUMBER_OF_CITIES) if not i == city]:
        distances[to_city][city] = \
            distances[city][to_city] = random.randint(50, 100)


if __name__ == '__main__':
    ps = problem_solution.ProblemSolution(
        INDIVIDUAL_SIZE, POPULATION_SIZE, N_ITERATIONS, N_MATINGS, distances)
    stats, population = ps.solve()

    print(population)

    fitnesses = sorted([
        (i, ps.toolbox.summarize_path(individual))
        for i, individual in enumerate(population)
    ], key=lambda x: x[1])

    print(fitnesses[:5])

    G = nx.from_numpy_matrix(distances)
    pos = nx.layout.spring_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=400,
                                   node_color="blue")

    labels = {i: i for i in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=15)

    edge_list = []
    for ind, el in enumerate(population[0]):
        if ind == len(population[0]) - 1:
            break
        edge_list.append((population[0][ind], population[0][ind + 1]))

    edges = nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(0,4), (4,1), (1,2), (2,3)],
        node_size=10,
        edge_color='black',
        edge_cmap=plt.cm.Blues,
        width=2,
    )

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()