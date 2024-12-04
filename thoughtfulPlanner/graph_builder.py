import networkx as nx
from geopy.distance import geodesic
from itertools import permutations

def build_graph(streets,edge=None):
    """
    Build a graph with optional edge attributes.
    
    Parameters:
    - streets: dict of street names and their coordinates
    - edge: callable, function to modify/add attributes to edges
    """
    G = nx.Graph()
    # Add nodes
    for name, coord in streets.items():
        G.add_node(name, pos=coord)
    
    # Add edges
    for (node_a, coord_a), (node_b, coord_b) in permutations(streets.items(), 2):
        distance = geodesic(coord_a, coord_b).km
        edge_data = {"distance": distance}
        
        # Apply edge modification logic if provided
        if edge is not None:
            edge_data.update(edge(node_a, coord_a, node_b, coord_b, distance))

        G.add_edge(node_a, node_b, **edge_data)

    return G

def build_graph_dijkstra(streets, transport_modes):
    """
    Build a graph for the fastest path with additional attributes.
    """
    def edge_modifier(node_a, coord_a, node_b, coord_b, distance):
        # Inline logic to calculate best mode and total time
        fastest_time = float('inf')
        best_mode = None
        
        for mode, data in transport_modes.items():
            speed = data["Speed_kmh"]
            transfer_time = data["Transfer_Time_min"]
            travel_time = (distance / speed) * 60  # Convert to minutes
            total_time = travel_time + transfer_time
            
            if total_time < fastest_time:
                fastest_time = total_time
                best_mode = mode

        return {"mode": best_mode, "total_time": fastest_time}
    
    return build_graph(streets, edge=edge_modifier)
