from route_finder import *


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
    map_renderer.save("map_test.html")


if __name__ == "__main__":
    main()