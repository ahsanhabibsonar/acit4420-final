def all_transports_path(graph, start_node, transport_modes):
    visited = set()
    path = [start_node]
    current_node = start_node
    total_cost = 0
    total_time = 0
    previous_mode = None  # Track the mode used for the previous segment
    transport_modes_used = []
    transfer_times_at_nodes = {}  # Track transfer times at nodes

    while len(visited) < len(graph.nodes):
        min_distance = float("inf")
        best_neighbor = None
        best_mode = None

        # Step 1: Find the shortest segment (distance-based) for the next step
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                distance = graph[current_node][neighbor]["distance"]
                if distance < min_distance:
                    min_distance = distance
                    best_neighbor = neighbor

        if best_neighbor is None:
            # No valid next node (disconnected graph case)
            break

        # Step 2: Determine the best mode for the shortest segment
        if min_distance >= 7:
            best_mode = "Train"
        elif 4 <= min_distance < 7:
            best_mode = "Bus"
        elif 2 <= min_distance < 4:
            best_mode = "Bicycle"
        else:
            best_mode = "Walking"

        # Calculate cost and time for the selected mode
        mode_data = transport_modes[best_mode]
        cost_per_km = mode_data["Cost_per_km"]
        speed_kmh = mode_data["Speed_kmh"]
        segment_cost = min_distance * cost_per_km
        segment_time = (min_distance / speed_kmh) * 60  # Convert hours to minutes
        total_cost += segment_cost
        total_time += segment_time

        # Update transfer time if mode changes
        if previous_mode and best_mode != previous_mode:
            transfer_time = transport_modes[previous_mode].get("Transfer_Time_min", 0)
            total_time += transfer_time

            # Add transfer time only for nodes except the start node
            if current_node != start_node:
                transfer_times_at_nodes[current_node] = transfer_time
                #print(f"Transfer at {current_node}: {transfer_time} min (Mode change: {previous_mode} -> {best_mode})")
        else:
            transfer_times_at_nodes[best_neighbor] = 0

        # Debugging output for selected mode, cost, and transfer time
        #print(f"Selected {current_node} -> {best_neighbor}: Mode={best_mode}, Distance={min_distance:.2f} km, "
        #      f"Cost=${segment_cost:.2f}, Segment Time={segment_time:.2f} min")

        # Step 3: Update path, visited nodes, and transport modes
        visited.add(current_node)
        path.append(best_neighbor)
        transport_modes_used.append(best_mode)
        current_node = best_neighbor
        previous_mode = best_mode  # Update the previous mode

    return path, transport_modes_used, total_cost, total_time, transfer_times_at_nodes

'''       
Define main Function

def main():
    
    #Format and print the terminal output
    #print(Fore.GREEN + "Optimized Path:" + Style.RESET_ALL, path)
    #print(Fore.YELLOW + f"Total Cost: ${total_cost:.2f}" + Style.RESET_ALL)
    #print(Fore.BLUE + f"Total Time: {total_time:.2f} minutes" + Style.RESET_ALL)
    
if __name__ == "__main__":
    main()

'''