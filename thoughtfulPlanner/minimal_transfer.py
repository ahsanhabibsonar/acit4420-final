def minimal_transfer(graph, start_node, transport_modes,alpha,beta,gamma):
    if not graph.nodes:  # Check if the graph is empty
        return [], [], 0, 0, {}
    """
    Find a continuous path starting at Yeouido, visiting all relatives,
    minimizing transfers, and tracking transfer time.
    """
    visited = set()
    path = [start_node]
    current_node = start_node
    transport_modes_used = []
    total_time = 0
    total_cost = 0
    transfer_times_at_nodes = {}  # To track transfer times at nodes
    previous_mode = None
    
    while len(visited) < len(graph.nodes) - 1:  # Exclude Yeouido itself from count
        #min_distance = float("inf")
        min_cost = float("inf")
        best_neighbor = None
        best_mode = None
        best_time = 0
        best_transfer_time = 0

        #print(f"Current Node: {current_node}")
        for neighbor in graph.neighbors(current_node):
            #if neighbor not in visited and neighbor != start_node:  # Exclude visited nodes and Yeouido
            if neighbor not in visited:    
                distance = graph[current_node][neighbor]["distance"]
                # Debugging
                # print(f"Evaluating: {current_node} -> {neighbor}, Distance: {distance:.2f} km")


                # Apply conditions for transport modes
                if distance >= 6:
                    mode = "Train"
                elif 3.5 <= distance < 6:
                    mode = "Bus"
                elif 1<= distance< 3.5:
                    mode = "Bicycle"
                else:
                    mode = "Walking"
                    
                #Calculate Travel Time
                speed = transport_modes[mode]["Speed_kmh"]
                travel_time = (distance / speed) * 60  # Convert hours to minutes
                
                # Calculate monetary cost
                cost = distance * transport_modes[mode]["Cost_per_km"]
                
                
                # Calculate transfer time (only if changing modes)
                transfer_time = (
                    transport_modes[previous_mode]["Transfer_Time_min"] 
                    if previous_mode and mode != previous_mode else 0
                )
                # Compute cost factor
                cost_factor = alpha * travel_time + beta * transfer_time + gamma * cost

                    
                # Select the neighbor with the minimum cost factor
                if cost_factor < min_cost:
                    min_cost = cost_factor
                    best_neighbor = neighbor
                    best_mode = mode
                    best_time = travel_time
                    best_transfer_time = transfer_time    

        if best_neighbor:
            visited.add(best_neighbor)
            path.append(best_neighbor)
            transport_modes_used.append(best_mode)
            
            # Update total time and cost
            segment_distance = graph[current_node][best_neighbor]["distance"]
            total_time += best_time + best_transfer_time # Add travel + transfer_time
            total_cost += segment_distance * transport_modes[best_mode]["Cost_per_km"]
            
            #print(f"Selected Edge: {current_node} -> {best_neighbor}, Mode: {best_mode}, Distance: {segment_distance:.2f} km")
            
        
            # Update transfer time if mode changes
                
            if previous_mode and best_mode != previous_mode:
                transfer_time = transport_modes[previous_mode].get("Transfer_Time_min", 0)
                total_time += transfer_time
                
                if current_node !=start_node:
                    transfer_times_at_nodes[current_node] = transfer_time
                    #print(f"Transfer at {current_node}: {transfer_time} min (Mode change: {previous_mode} -> {best_mode})")
            else:
                transfer_times_at_nodes[best_neighbor] = 0
            
            # Update current node and mode    
            previous_mode = best_mode
            current_node = best_neighbor
            
        else:
            print("No valid path found")
            break
     
    return path, transport_modes_used, total_time, total_cost, transfer_times_at_nodes

