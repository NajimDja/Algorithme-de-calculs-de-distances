import heapq

# Chaque clé = sommet
# Chaque valeur = liste de (voisin, poids)

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 1)],
    'D': []
}

def dijkstra(graph, start):
    # Initialisation
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    priority_queue = [(0, start)]  # (distance, noeud)
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Si on a déjà trouvé mieux, on ignore
        if current_distance > distances[current_node]:
            continue
        
        # Explorer les voisins
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

result = dijkstra(graph, 'A')
print(result)