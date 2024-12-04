import networkx as nx
import random
import time
from minimal_transfer import minimal_transfer

# Create a graph with 500 nodes and 2000 edges
def create_connected_graph(num_nodes, num_edges):
    G = nx.gnm_random_graph(num_nodes, num_edges)
    
    # Ensure all nodes are connected (bridging components if necessary)
    if not nx.is_connected(G):
        components = list(nx.connected_components(G))
        print(f"Number of connected components: {len(components)}")
        print("Adding bridging edges to ensure connectivity.")
        
        for i in range(len(components) - 1):
            node_a = list(components[i])[0]
            node_b = list(components[i + 1])[0]
            G.add_edge(node_a, node_b, distance=random.uniform(1, 10))
    
    # Add random distances as edge attributes
    for (u, v) in G.edges():
        G.edges[u, v]["distance"] = round(random.uniform(1, 10), 2)  # Random distances between 1-10 km
    
    return G

# Test the performance of the Minimal Transfer algorithm
def test_minimal_transfer_performance():
    num_nodes = 500
    num_edges = 2000

    # Step 1: Create a connected graph
    G = create_connected_graph(num_nodes, num_edges)
    print(f"Total nodes in graph: {G.number_of_nodes()}")
    print(f"Total edges in graph: {G.number_of_edges()}")

    # Step 2: Define a start node and ensure it exists
    start_node = "0"
    if start_node not in G.nodes:
        print(f"Node {start_node} not found. Adding it to the graph.")
        G.add_node(start_node)
        # Connect to a random node to maintain connectivity
        random_node = random.choice(list(G.nodes))
        G.add_edge(start_node, random_node, distance=random.uniform(1, 10))

    # Step 3: Define transport modes
    transport_modes = {
        "Walking": {"Speed_kmh": 5, "Cost_per_km": 0, "Transfer_Time_min": 0},
        "Bicycle": {"Speed_kmh": 15, "Cost_per_km": 0, "Transfer_Time_min": 2},
        "Bus": {"Speed_kmh": 40, "Cost_per_km": 1, "Transfer_Time_min": 5},
        "Train": {"Speed_kmh": 80, "Cost_per_km": 2, "Transfer_Time_min": 10}
    }

    # Step 4: Measure performance
    print("Running Minimal Transfer Algorithm...")
    start_time = time.time()
    path, transport_modes_used, total_cost, total_time, transfer_times = minimal_transfer(
        G, start_node, transport_modes, alpha=1, beta=2, gamma=3
    )
    execution_time = time.time() - start_time

    # Step 5: Output results
    print(f"Execution time for Minimal Transfer: {execution_time:.6f} seconds")
    print(f"Path length: {len(path)} nodes")

# Run the test
if __name__ == "__main__":
    test_minimal_transfer_performance()
