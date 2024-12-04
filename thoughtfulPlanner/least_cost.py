def find_min_cost(graph, start_node, transport_modes):
    """
    Finds the shortest path using Dijkstra's algorithm and assigns the most economical transport mode
    to each segment of the path.
    """
    visited = set()
    path = [start_node]
    current_node = start_node
    total_cost = 0
    total_time = 0 # To track Time
    transport_modes_used = []
    transfer_times = {}

    while len(visited) < len(graph.nodes) - 1:  # Exclude the start node itself from count
        min_distance = float("inf")
        best_neighbor = None

        # Step 1: Find the shortest segment (distance-based) for the next step
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                distance = graph[current_node][neighbor]["distance"]
                if distance < min_distance:
                    min_distance = distance
                    best_neighbor = neighbor

        # If no valid neighbors are found, break out of the loop
        if not best_neighbor:
            print("No valid neighbors found. Stopping.")
            break

        # Step 2: Select the most economical mode for the shortest segment
        min_cost = float("inf")
        best_mode = None
        for mode, mode_data in transport_modes.items():
            cost_per_km = mode_data["Cost_per_km"]
            segment_cost = min_distance * cost_per_km
            segment_time = (min_distance / mode_data["Speed_kmh"]) * 60  # Convert hours to minutes
            if segment_cost < min_cost:
                min_cost = segment_cost
                best_mode = mode
                best_time = segment_time
        # Step 3: Update path, visited nodes, total cost, and transport modes
        visited.add(best_neighbor)
        path.append(best_neighbor)
        transport_modes_used.append(best_mode)
        total_cost += min_cost
        total_time+= best_time
        # Transfer time is not considered here, but can be initialized as zero
        transfer_times[best_neighbor] = 0

        # Debugging output for selected mode and cost
        #print(f"Selected {current_node} -> {best_neighbor}: Mode={best_mode}, Distance={min_distance:.2f} km, Cost=${min_cost:.2f}")

        # Move to the next node
        current_node = best_neighbor

    return path, transport_modes_used, total_cost, total_time, transfer_times

