import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

graph = nx.Graph()
graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
graph.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 8), (6, 8), (7, 8)])


# busca por largura

def breadth_first_search(initial_node):

    if initial_node not in graph.nodes:
        raise Exception('O vértice informado não existe no grafo')

    # inicializacao
    sequence = []
    queue = deque([initial_node])
    for node in graph.nodes:
        graph.nodes[node]['color'] = 'white'
    graph.nodes[initial_node]['color'] = 'gray' 

    while queue:
        node = queue[0]
        neighbors = filter(lambda x: graph.nodes[x]['color'] is not 'black', graph.neighbors(node)) 
        for n in neighbors: # vizinhos
            if graph.nodes[n]['color'] == 'white':
                graph.nodes[n]['color'] = 'gray'
                queue.append(n) # adiciona o elemento no final da fila

        graph.nodes[node]['color'] = 'black'
        sequence.append(node)
        queue.popleft() # remove o primeiro elemento
    
    if len(sequence) != len(graph):
        print('O grafo é disconexo.')

    return sequence

# print(breadth_first_search(1))


def deep_first_search(initial_node):
    sequence = []
    stack = deque([initial_node])

    for g in graph.nodes:
        graph.nodes[g]['color'] = 'white'
    graph.nodes[initial_node]['color'] = 'gray'

    while stack:
        node = stack[0]
        neighbors = [n for n in graph.neighbors(node) if graph.nodes[n]['color'] == 'white']
        if neighbors:
            next_node = neighbors[0]
            graph.nodes[next_node]['color'] = 'gray'
            stack.appendleft(next_node)
        else:
            graph.nodes[node]['color'] = 'black'
            stack.popleft()
        
            sequence.append(node)

    sequence.reverse()
    return sequence


# nx.draw(graph, with_labels=True)
# plt.show()  

print(deep_first_search(1))