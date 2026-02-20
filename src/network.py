###############################################################
# Script d'exploration et découverte de la librairie NetworkX #
###############################################################

import networkx as nx
import matplotlib.pyplot as plt

def visualiser_graph(graph, title : str = ""):
    plt.title(title)
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

# visualiser_graph(GG)

# Chemin le plus court entre deux noeuds
print(nx.shortest_path(GG, 1, 3))

######################################
# Génération de graphs et opérations #
######################################

# Application d'opérations classiques sur les graphs

"""
subgraph(G, nbunch) : Returns the subgraph induced on nodes in nbunch.
union(G, H[, rename]) : Combine graphs G and H.
disjoint_union(G, H) : Combine graphs G and H.
cartesian_product(G, H) : Returns the Cartesian product of G and H.
compose(G, H) : Compose graph G with H by combining nodes and edges into a single graph.
complement(G) : Returns the graph complement of G.
create_empty_copy(G[, with_data]) : Returns a copy of the graph G with all of the edges removed.
to_undirected(graph) : Returns an undirected view of the graph graph.
to_directed(graph) : Returns a directed view of the graph graph.
"""

# Utilisation d'un appel à l'un des petits graphiques classiques

PG = nx.petersen_graph()
visualiser_graph(PG, title="Petersen Graph")

TG = nx.tutte_graph()
# visualiser_graph(TG, title="Tutte Graph")

SMG = nx.sedgewick_maze_graph()
# visualiser_graph(SMG, title="Sedgewick Maze Graph")

THG = nx.tetrahedral_graph()
# visualiser_graph(THG, title="Tetrahedral Graph")

# Utilisation d'un générateur (constructif) pour un graphe classique

K_5 = nx.complete_graph(5) # Tous les noeuds sont repliés
K_3_5 = nx.complete_bipartite_graph(3, 5) # 3 noeuds sont connéctés aux 5 autres
barbell = nx.barbell_graph(10, 10) # 2 complete graph reliés par un chemin
lollipop = nx.lollipop_graph(10, 20)

# Utilisation d'un générateur de graph stochastique

er = nx.erdos_renyi_graph(100, 0.15) # Erdős-Rényi graph or a binomial graph.
ws = nx.watts_strogatz_graph(30, 3, 0.1) # Returns a Watts–Strogatz small-world graph.
ba = nx.barabasi_albert_graph(100, 5) # Returns a random graph using Barabási–Albert preferential attachment
red = nx.random_lobster_graph(10, 0.7, 0.9) # Returns a random lobster graph.

# Enregistrer et lire un graph dans un fichier
# nx.write_gml(red, "maps/random_lobster_graph.gml")
# mygraph = nx.read_gml("maps/random_lobster_graph.gml")

# visualiser_graph(mygraph)

#####################
# Analyse de graphs #
#####################

print("\nAnalyse de graph")

G = nx.Graph()
G.add_edges_from([(1,2), (1,3)])
G.add_node("spam")
print(list(nx.connected_components(G)))

print(sorted(d for n,d in G.degree()))

print(nx.clustering(G))

sp = dict(nx.all_pairs_shortest_path(G))
print(sp[3])

############################################################
# Considérations relatives aux nombres à virgule flottante #
############################################################

tiny = 5e-17

G = nx.DiGraph()
G.add_edge('A', 'B', weight=0.1)
G.add_edge('B', 'C', weight=0.1)
G.add_edge('C', 'D', weight=0.1)
G.add_edge('A', 'D', weight=0.3 + tiny)

path = nx.shortest_path(G, source='A', target='D', weight='weight')
print(path)

for precision in [16, 17]:
    path = nx.shortest_path(
        G,
        source='A',
        target='D',
        weight=lambda u, v, d: int(d['weight'] * 10 ** precision)
    )
    print(f"With {precision} precision digits, path is {path}")

#########################
# Visualiser les graphs #
#########################

G = nx.petersen_graph()
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()

options = {
    'node_color': 'black',
    'node_size': 100,
    'width': 3,
}
subax1 = plt.subplot(221)
nx.draw_random(G, **options)
subax2 = plt.subplot(222)
nx.draw_circular(G, **options)
subax3 = plt.subplot(223)
nx.draw_spectral(G, **options)
subax4 = plt.subplot(224)
nx.draw_shell(G, nlist=[range(5,10), range(5)], **options)
plt.show()

G = nx.dodecahedral_graph()
shells = [[2, 3, 4, 5, 6], [8, 1, 0, 19, 18, 17, 16, 15, 14, 7], [9, 10, 11, 12, 13]]
nx.draw_shell(G, nlist=shells, **options)
plt.show()