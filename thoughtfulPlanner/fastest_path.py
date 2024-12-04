
from logger import logger

def find_fastest_path(graph, start_node, transport_modes):
    
    
    # Get user inputs for constraints
    try:
        max_time = input("Enter maximum travel time per segment (leave blank for no limit): ")
        max_time = float(max_time) if max_time else None

        max_cost = input("Enter maximum cost per segment (leave blank for no limit): ")
        max_cost = float(max_cost) if max_cost else None
    except ValueError as e:
        logger.error(f"Invalid input for max_time: {e}")
        print("Invalid input. Using default value.")
        max_time = None
        max_cost = None
    
    """
    Combines Dijkstra’s algorithm and GNN to find the fastest path based on time and distance.
    """
    visited = set()
    path = [start_node]
    current_node = start_node
    total_time = 0
    total_cost = 0
    transport_modes_used = []
    transfer_times_at_nodes = {}  # To track transfer times at nodes
    previous_mode = None

    while len(visited) < len(graph.nodes) - 1:  # Exclude start_node itself from count
        min_time = float("inf")
        #min_cost = float("inf")
        best_neighbor = None
        best_mode = None
        best_time = 0
        #best_cost = 0

        #print(f"Current Node: {current_node}")
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                edge_data = graph[current_node][neighbor]
                distance = edge_data["distance"]
                
                # Get valid transport modes based on user constraints
            valid_modes = [
                (mode, (distance / mode_data["Speed_kmh"]) * 60, distance * mode_data["Cost_per_km"])
                for mode, mode_data in transport_modes.items()
                if (not max_time or (distance / mode_data["Speed_kmh"]) * 60 <= max_time)
                and (not max_cost or distance * mode_data["Cost_per_km"] <= max_cost)
                
            ]
            
            #print(f"Valid Modes for {current_node} -> {neighbor}: {valid_modes}")
            
            if valid_modes:
                # Prioritize cost if constraints are set, otherwise prioritize time
                if max_cost or max_time:
                    best_mode, travel_time, cost = min(valid_modes, key=lambda x: (x[2], x[1]))
                else:
                    best_mode, travel_time, cost = min(valid_modes, key=lambda x: (x[1], x[2]))
                    # Sort modes by travel time, then cost, and select the best
                

            # Calculate transfer time if mode changes
                transfer_time = (
                transport_modes[previous_mode]["Transfer_Time_min"] 
                if previous_mode and best_mode != previous_mode else 0
                )

            total_time_factor = travel_time + transfer_time


            if total_time_factor < min_time:
                min_time = total_time_factor
                best_neighbor = neighbor
                best_mode = best_mode
                best_time = travel_time
                #best_cost = cost
            else:
                #print(f"No valid modes for {current_node} -> {neighbor}. Skipping.")
                continue
                        
                        

        if best_neighbor:
            visited.add(best_neighbor)
            path.append(best_neighbor)
            transport_modes_used.append(best_mode)
            total_time += best_time
            #total_cost += best_cost
            
            # Calculate transfer time if the mode changes
            if previous_mode and best_mode != previous_mode:
                transfer_time = transport_modes[previous_mode]["Transfer_Time_min"]
                total_time += transfer_time
                transfer_times_at_nodes[current_node] = transfer_time
                #print(f"Transfer at {current_node}: {transfer_time} min (Mode change: {previous_mode} -> {best_mode})")

            else:
                transfer_times_at_nodes[current_node] = 0
            
            total_cost += graph[current_node][best_neighbor]["distance"] * transport_modes[best_mode]["Cost_per_km"]
            
            #print(f"Selected: {current_node} -> {best_neighbor}, Mode: {best_mode}, Time: {best_time:.2f}, Cost: {total_cost:.2f}")
            previous_mode = best_mode
            current_node = best_neighbor
        else:
            #print("No valid path found.")
            break
    
    if current_node not in transfer_times_at_nodes:
        transfer_times_at_nodes[current_node] = 0
    '''
    print(f"Path: {path}")
    print(f"Transport Modes Used: {transport_modes_used}")
    print(f"Total Time: {total_time}")
    print(f"Total Cost: {total_cost}")
    print(f"Transfer Times at Nodes: {transfer_times_at_nodes}")
    '''

    total_transfer_time = sum(transfer_times_at_nodes.values())
    #print(f"Total Transfer Time: {total_transfer_time:.2f} min")
    return path, transport_modes_used,total_time,total_cost, transfer_times_at_nodes

