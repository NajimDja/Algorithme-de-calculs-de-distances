import networkx as nx
import matplotlib.pyplot as plt

def visualiser_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()

# Création d'un graph "G"
G = nx.Graph()

##############
# Les noeuds #
##############

# Ajouter un noeud au graph
G.add_node(1)

# Ajouter des noeuds d'un itérable comme une liste
G.add_nodes_from([2, 3])

# Ajouter des noeuds avec des attributs associés forme : (node, node_attribut_dict)
G.add_nodes_from([(4, {"color":"red"}), (5, {"color":"green"})])

# Les noeuds d'un graph peuvent être incorporés à un autre
H = nx.path_graph(10)
G.add_nodes_from(H)
G.add_node(H)

# Visualiser le graph
# nx.draw(G, with_labels=True)
# plt.show()

###############
# Les arrêtes #
###############

G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e) #unpack edge tuple

# Ajouter via une liste d'arrêtes
G.add_edges_from([(1, 2), (1, 3)])
G.add_edges_from(H.edges)

# Visualiser le graph
# nx.draw(G, with_labels=True)
# plt.show()

# Effacer tout les noeuds et arrêtes
G.clear()

# Ajout de nouveaux noeuds et arrêtes, nx ignore ceux déjà présents
G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

# Obtenir le nombre de noeuds et d'arrêtes d'un graph
print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre d'arrêtes :", G.number_of_edges())

DG = nx.DiGraph()
DG.add_edge(2, 1)   # adds the nodes in order 2, 1
DG.add_edge(1, 3)
DG.add_edge(2, 4)
DG.add_edge(1, 2)
assert list(DG.successors(2)) == [1, 4]
assert list(DG.edges) == [(2, 1), (2, 4), (1, 3), (1, 2)]

# Visualiser le graph
# nx.draw(DG, with_labels=True)
# plt.show()

####################################
# Examiner les éléments d'un graph #
####################################

print(list(G.nodes))
print(list(G.edges))
print(list(G.adj[1]))  # or list(G.neighbors(1))
print(G.degree[1])  # the number of edges incident to 1

print(G.edges([2, 'm']))
print(G.degree([2, 3]))

########################
# Accéder aux patterns #
########################

# Utile pour modifier ou fixer des paramètres
G.nodes["spam"]["color"] = "blue"
G.edges[(1, 2)]["weight"] = 10

print("EdgesDataView :", G.edges(data=True))
print("NodeDataView :", G.nodes(data="color"))

#################################
# Effacer des éléments du graph #
#################################

G.remove_node(2)
G.remove_nodes_from("spam")
print(list(G.nodes))
print(list(G.edges))

G.remove_edge(1, 3)
print(list(G.nodes))
print(list(G.edges), '\n')

#####################################
# Utiliser le constructeur de graph #
#####################################

# create a DiGraph using the connections from G
G.add_edge(1, 2)
H = nx.DiGraph(G)  
print(list(H.edges()))

# nx.draw(H, with_labels=True)
# plt.show()

# create a graph from an edge list
edgelist = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edgelist)  
print(list(H.edges()))

# nx.draw(H, with_labels=True)
# plt.show()

# create a Graph dict mapping nodes to nbrs
adjacency_dict = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
H = nx.Graph(adjacency_dict)  
print(list(H.edges()))

# nx.draw(H, with_labels=True)
# plt.show()

###################################
# Accéder aux arrêtes et voisions #
###################################

G = nx.Graph([(1, 2, {"color": "yellow"})])
print(G[1]) # same as G.adj[1]
print(G[1][2])
print(G.edges[1, 2])

G.add_edge(1, 3)
G[1][3]['color'] = "blue"
G.edges[1, 2]['color'] = "red"
print(G.edges[1, 2])

# Examination des pairs (noeuds/adjency)
FG = nx.Graph()
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])

for n, nbrs in FG.adj.items():
   for nbr, eattr in nbrs.items():
       wt = eattr['weight']
       if wt < 0.5: 
          print(f"({n}, {nbr}, {wt:.3})")

for (u, v, wt) in FG.edges.data('weight'):
    if wt < 0.5:
        print(f"({u}, {v}, {wt:.3})")

#######################################################
# Ajouter des attributs aux graphs, noeuds et arrêtes #
#######################################################

# Assigner un attribut en créant un nouveau graph
G = nx.Graph(day="Friday")
print(G.graph)

# Modification
G.graph['day'] = "Monday"
G.graph

# Attributs des noeuds
G.add_node(1, time='5pm')
G.add_nodes_from([3], time='2pm')
print(G.nodes[1])

G.nodes[1]['room'] = 714
print(G.nodes.data())

# Attributs des arêtes
G.add_edge(1, 2, weight=4.7 )
G.add_edges_from([(3, 4), (4, 5)], color='red')
G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
G[1][2]['weight'] = 4.7
G.edges[3, 4]['weight'] = 4.2
print(G.edges.data())

######################
# Graph Directionnel #
######################

DG = nx.DiGraph()
DG.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75)])

print(DG.out_degree(1, weight='weight'))
print(DG.degree(1, weight='weight'))

print(list(DG.successors(1)))
print(list(DG.neighbors(1)))

H = nx.Graph(DG)  # create an undirected graph H from a directed graph G
# visualiser_graph(DG)
# visualiser_graph(H)

###############
# Multigraphs #
###############

MG = nx.MultiGraph()
MG.add_weighted_edges_from([(1, 2, 0.5), (1, 2, 0.75), (2, 3, 0.5)])
print(dict(MG.degree(weight='weight')))
# visualiser_graph(MG)

GG = nx.Graph()
for n, nbrs in MG.adjacency():
   for nbr, edict in nbrs.items():
       minvalue = min([d['weight'] for d in edict.values()])
       GG.add_edge(n, nbr, weight = minvalue)

visualiser_graph(GG)

# Chemin le plus court entre deux noeuds
print(nx.shortest_path(GG, 1, 3))