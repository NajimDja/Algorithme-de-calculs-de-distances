# Application des algorithmes entre deux destinations

import osmnx as ox
import networkx as nx
import folium
import os
import heapq
import streamlit as st
import time
from streamlit_folium import st_folium


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
        print("1 - Téléchargement du graphe OSM.")
        return ox.graph_from_place(self.place, network_type=self.network_type)

    def geocode_to_node(self, address: str) -> int:
        """
        Géocode une adresse et renvoie le nœud le plus proche dans le graphe.
        """
        print(f"2 - Géocodage de l'addresse '{address}' et récupération du noeud le plus proche.")
        lat, lon = ox.geocode(address)
        node = ox.distance.nearest_nodes(self.graph, lon, lat)
        return node

    def shortest_path_dijkstra(self, origin_node: int, dest_node: int, weight: str = "length"):
        """
        Calcule le plus court chemin avec Dijkstra.
        """
        print("3 - Calcul du chemin le plus court avec Dijkstra")
        return nx.shortest_path(self.graph, origin_node, dest_node, weight=weight)

    def shortest_path_astar(self, origin_node: int, dest_node: int, weight: str = "length"):
        """
        Calcule le plus court chemin avec A*.
        """
        print("3 - Calcul du chemin le plus court avec A*")
        return nx.astar_path(self.graph, origin_node, dest_node, weight=weight)

    def get_route_coords(self, route):
        """
        Convertit une liste de nœuds en liste de coordonnées (lat, lon).
        """
        print("4 - Convertit la liste de noeuds en liste de coordonnées")
        return [(self.graph.nodes[node]["y"], self.graph.nodes[node]["x"]) for node in route]

    def dijkstra_steps(self, origin_node: int, dest_node: int, weight: str = "length"):
        """
        Version pas-à-pas de Dijkstra pour visualisation.
        Yield les noeuds explorés à chaque étape.
        """
        graph = self.graph
        distances = {node: float("inf") for node in graph.nodes}
        distances[origin_node] = 0

        visited = set()
        pq = [(0, origin_node)]
        parents = {}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue

            visited.add(current_node)

            # on renvoie les noeuds explorés
            yield visited, None  

            if current_node == dest_node:
                break

            for neighbor in graph.neighbors(current_node):
                edge_data = graph.get_edge_data(current_node, neighbor)
                length = edge_data[0].get(weight, 1)

                new_distance = current_distance + length

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parents[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))

        # Reconstruction du chemin final
        path = []
        node = dest_node
        while node in parents:
            path.append(node)
            node = parents[node]
        path.append(origin_node)
        path.reverse()

        yield visited, path


class MapRenderer:

    def __init__(self, center: tuple, zoom_start: int = 14):
        """
        Initialise la carte Folium.
        center : (lat, lon)
        """
        self.path = "maps"
        print("5 - Création de la carte.")
        self.map = folium.Map(location=center, zoom_start=zoom_start)

    def add_route(self, route_coords, color: str = "red", weight: int = 5):
        """
        Ajoute une polyline représentant l'itinéraire à la carte.
        """
        print("6 - Ajout de l'itinéraire à la carte.")
        folium.PolyLine(route_coords, color=color, weight=weight).add_to(self.map)

    def save(self, name: str):
        """
        Sauvegarde la carte dans un fichier HTML.
        """
        print("7 - Sauvegarde de la carte au format html.")
        filepath = os.path.join(self.path, name)
        self.map.save(filepath)



class StreamlitApp:

    def __init__(self, route_finder):
        self.route_finder = route_finder

    def run(self):

        st.title("Visualisation Dijkstra en direct")

        origin_address = st.text_input("Adresse de départ", "Tour Eiffel, Paris")
        destination_address = st.text_input("Adresse d'arrivée", "Musée du Louvre, Paris")

        if "running" not in st.session_state:
            st.session_state.running = False

        if st.button("Lancer l'algorithme"):
            st.session_state.running = True

        if st.session_state.running:

            orig_node = self.route_finder.geocode_to_node(origin_address)
            dest_node = self.route_finder.geocode_to_node(destination_address)

            origin_lat, origin_lon = ox.geocode(origin_address)

            # 1 placeholder
            map_placeholder = st.empty()

            for visited, path in self.route_finder.dijkstra_steps(orig_node, dest_node):

                m = folium.Map(location=(origin_lat, origin_lon), zoom_start=14)

                # Noeuds explorés
                for n in visited:
                    lat = self.route_finder.graph.nodes[n]["y"]
                    lon = self.route_finder.graph.nodes[n]["x"]

                    folium.CircleMarker(
                        location=(lat, lon),
                        radius=2,
                        color="blue",
                        fill=True,
                        fill_opacity=0.6
                    ).add_to(m)

                # Chemin final
                if path:
                    route_coords = self.route_finder.get_route_coords(path)
                    folium.PolyLine(route_coords, color="red", weight=5).add_to(m)

                # on remplace le contenu du placeholder
                with map_placeholder:
                    st_folium(m, width=700, height=500)

                time.sleep(0.05)

            st.session_state.running = False