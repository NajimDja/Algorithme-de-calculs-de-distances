# Application des algorithmes entre deux destinations

import osmnx as ox
import networkx as nx
import folium
import os

class RouteFinder:

    def __init__(self, place: str, network_type: str = "drive"):
        """
        Initialise le graphe routier pour un lieu donné.
        """
        self.place = place
        self.network_type = network_type
        self.graph = self._load_graph()

    def _load_graph(self):
        """
        Télécharge / charge le graphe OSM pour le lieu.
        """
        return ox.graph_from_place(self.place, network_type=self.network_type)

    def geocode_to_node(self, address: str) -> int:
        """
        Géocode une adresse et renvoie le nœud le plus proche dans le graphe.
        """
        lat, lon = ox.geocode(address)
        node = ox.distance.nearest_nodes(self.graph, lon, lat)
        return node

    def shortest_path_dijkstra(self, origin_node: int, dest_node: int, weight: str = "length"):
        """
        Calcule le plus court chemin avec Dijkstra.
        """
        return nx.shortest_path(self.graph, origin_node, dest_node, weight=weight)

    def shortest_path_astar(self, origin_node: int, dest_node: int, weight: str = "length"):
        """
        Calcule le plus court chemin avec A*.
        """
        return nx.astar_path(self.graph, origin_node, dest_node, weight=weight)

    def get_route_coords(self, route):
        """
        Convertit une liste de nœuds en liste de coordonnées (lat, lon).
        """
        return [(self.graph.nodes[node]["y"], self.graph.nodes[node]["x"]) for node in route]

class MapRenderer:

    def __init__(self, center: tuple, zoom_start: int = 14):
        """
        Initialise la carte Folium.
        center : (lat, lon)
        """
        self.path = "maps"
        self.map = folium.Map(location=center, zoom_start=zoom_start)

    def add_route(self, route_coords, color: str = "red", weight: int = 5):
        """
        Ajoute une polyline représentant l'itinéraire à la carte.
        """
        folium.PolyLine(route_coords, color=color, weight=weight).add_to(self.map)

    def save(self, name: str):
        """
        Sauvegarde la carte dans un fichier HTML.
        """
        filepath = os.path.join(self.path, name)
        self.map.save(filepath)


def main():

    # 1. Initialiser le calculateur de routes pour Paris
    route_finder = RouteFinder("Paris, France", network_type="drive")

    # 2. Définir les adresses
    origin_address = "Tour Eiffel, Paris"
    destination_address = "Louvre Museum, Paris"

    # 3. Géocodage vers nœuds
    orig_node = route_finder.geocode_to_node(origin_address)
    dest_node = route_finder.geocode_to_node(destination_address)

    # 4. Calcul de l’itinéraire
    # Dijkstra
    # route = route_finder.shortest_path_dijkstra(orig_node, dest_node, weight="length")
    
    # A* :
    route = route_finder.shortest_path_astar(orig_node, dest_node, weight="length")

    # 5. Récupérer les coordonnées de l’itinéraire
    route_coords = route_finder.get_route_coords(route)

    # 6. Créer la carte centrée sur l’origine
    origin_lat, origin_lon = ox.geocode(origin_address)
    map_renderer = MapRenderer(center=(origin_lat, origin_lon), zoom_start=14)

    # 7. Ajouter la route à la carte
    map_renderer.add_route(route_coords, color="red", weight=5)

    # 8. Sauvegarder la carte
    map_renderer.save("map_astar.html")


if __name__ == "__main__":
    main()