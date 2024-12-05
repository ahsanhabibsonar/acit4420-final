import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import networkx as nx


def plot_graph(graph, path, transport_modes_used, transfer_times,transport_modes,title_text):
    
    """
    Plots the graph with edges colored by transport mode and displays transfer times at nodes.
    Includes Total Time, Total Distance, and Total Transfer Time in the title.
    """
    # Calculate total transfer time
    total_transfer_time = sum(transfer_times.values())

    # Calculate total distance
    total_distance = sum(
        graph[path[i]][path[i + 1]]["distance"] for i in range(len(path) - 1)
    )
    
    total_time = sum(
    (graph[path[i]][path[i + 1]]["distance"] * 60) / 
    transport_modes[transport_modes_used[i]]["Speed_kmh"] for i in range(len(path) - 1)
    ) + total_transfer_time
    
    total_cost = sum(
    graph[path[i]][path[i + 1]]["distance"] * transport_modes[transport_modes_used[i]]["Cost_per_km"]
    for i in range(len(path) - 1)
    )
    
    
    for i in range(len(path) - 1):
        distance = graph[path[i]][path[i + 1]]["distance"]
        mode = transport_modes_used[i]
        cost_per_km = transport_modes[mode]["Cost_per_km"]
        segment_cost = distance * cost_per_km
        #print(f"Segment {path[i]} -> {path[i + 1]}: Mode={mode}, Distance={distance:.2f} km, Cost={segment_cost:.2f}")
    


    # Extract positions of Nodes
    positions = nx.get_node_attributes(graph, "pos")
   # print("Node Positions:", positions)
    
    plt.figure(figsize=(14, 10))
    # Adjust subplot margins
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    
    #print("Path Edges:", path_edges)

    
    # Draw Nodes
    nx.draw_networkx_nodes(graph, pos=positions, node_size=300, node_color="skyblue", alpha=0.5)
    # Draw nodes with different shapes and colors
    nx.draw_networkx_nodes(graph, pos=positions, nodelist=["Yeouido"], node_size=300, node_color="cyan", node_shape='s')
    #nx.draw_networkx_labels(G, pos=positions, labels={"Yeouido": "Yeouido"})

    # Transparent Node Labels (manual)
    for node, (x, y) in positions.items():
        label = node
        plt.text(
            x, y + 0.006,
            label,
            fontsize=8,
            weight="normal",
            alpha=0.8,
            horizontalalignment="center",
            verticalalignment="center",
        )

    # Draw Labels
    #nx.draw_networkx_labels(graph, pos=positions, font_size=7, font_weight="normal")
    
    # Draw edges with colors based on transport modes
    #path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    for idx, edge in enumerate(path_edges):
        start_node, end_node = edge
        mode = transport_modes_used[idx]
        color = transport_modes[mode]["Color"]
        nx.draw_networkx_edges(graph, pos=positions, edgelist=[edge], edge_color=color, width=2, alpha=0.3)

    # Add edge labels with distance
      
    edge_labels = {
        (u, v): f"{graph[u][v]['distance']:.2f} km" for u, v in path_edges if graph[u][v]['distance']>2
    }
    
    nx.draw_networkx_edge_labels(graph, pos=positions, edge_labels=edge_labels, font_size=8)  # Semi-transparent background for labels

    # Add transfer times on nodes
    for node, transfer_time in transfer_times.items():
        if transfer_time > 0:
            x, y = positions[node]
            plt.text(x + 0.001, y + 0.002, f"{transfer_time} min", fontsize=8, color="darkred",alpha=0.5)

    # Dynamic axis labels based on Longitude and Latitude range
    
    longitudes = [pos[1] for pos in positions.values()]
    latitudes = [pos[0] for pos in positions.values()]
    
    
    plt.xlabel(f"Longitude: {min(longitudes):.4f} - {max(longitudes):.4f}",fontsize=12)
    plt.ylabel(f"Latitude: {min(latitudes):.4f} - {max(latitudes):.4f}",fontsize=12)
    

    # Add a legend for transport modes
    import matplotlib.patches as mpatches
    
    legend_labels = {mode: transport_modes[mode]["Color"] for mode in transport_modes}
    transport_patches = [mpatches.Patch(color=color, label=mode) for mode, color in legend_labels.items()]

    # Legend for special nodes
    node_patches = [
        mlines.Line2D([], [], color="cyan", marker="s", markersize=10, linestyle="None", label="Yeouido"),
        mlines.Line2D([], [], color="skyblue", marker="o", markersize=10, linestyle="None", label="Streets"),
    ]
    
    # Combine legends
    plot_patches = transport_patches + node_patches

    # Add title with Total Time, Total Distance, and Total Transfer Time
    plt.title(
        f"{title_text}\n" 
        f"Total Time: {total_time:.2f} min | Total Distance: {total_distance:.2f} km | "
        f"Total Transfer Time: {total_transfer_time:.2f} min | Total Cost: ${total_cost:.2f}",
        fontsize=14
    )


    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend(handles=plot_patches, title="Transport Modes\nand Locations", loc="upper right")


    # Display the plot
    #plt.tight_layout()
    plt.show()
    
