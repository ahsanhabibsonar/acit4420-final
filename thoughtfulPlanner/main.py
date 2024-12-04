# main.py
from minimal_transfer import minimal_transfer
from fastest_path import find_fastest_path
from least_cost import find_min_cost
from data_loader import load_transport_modes,add_coordinates
from graph_builder import build_graph, build_graph_dijkstra
from plotting import plot_graph
from all_transport_modes import all_transports_path
import time

def main_menu():
    print("\n--- Main Menu ---")
    print("1. Run Minimal Transfer")
    print("2. Run Fastest Route")
    print("3. Run Least Cost")
    print("4. Run All Transports Path")
    print("5. Exit")
    choice = input("Enter your choice: ")
    return choice.strip()
    print(f"Transfer Times at Nodes: {transfer_times}")

def std_print(path,transport_modes_used,total_time,total_cost,transfer_times,execution_time=None):
    print(f"Path: {path}")
    print(f"Transport Modes Used: {transport_modes_used}")
    print(f"Total Time: {total_time:.2f} minutes")
    print(f"Total Cost: ${total_cost:.2f}")
    print(f"Transfer Times at Nodes: {transfer_times}")
    if execution_time is not None:
        print(f"Execution Time:{execution_time:.6f}seconds")
            


def main():
    # Load data
    transport_modes = load_transport_modes("transport_modes.csv")
    streets= add_coordinates(max_distance_km=20)

    G=build_graph(streets)
    G = build_graph_dijkstra(streets, transport_modes)
    while True:
        choice = main_menu()

        if choice == "1":
            title_text = "Minimal Transfer Optimization"
            print("\n--- Minimal Transfer ---")
            print("Higher alpha prioritizes faster travel.")
            print("Higher beta prioritizes less transfer.")
            print("Higher gamma prioritizes saving cost.")
            #print("In case of blank input, program will use default values.")
            #alpha = float(input("Enter weight for travel time (alpha): "))
            try:
                alpha = float(input("Enter weight for travel time (alpha): "))
            except ValueError:
                alpha = 1.0  # Default value
                print("Invalid input. Default value (alpha=1.0) is used.")
            try:    
                beta = float(input("Enter weight for transfer time (beta): "))
            except ValueError:
                beta = 1.0  # Default value
                print("Invalid input. Default value (beta=1.0) is used.")
            try:    
                gamma = float(input("Enter weight for cost (gamma): "))
            except ValueError:
                gamma = 1.0  # Default value
                print("Invalid input. Default value (gamma=1.0) is used.")
            
            start_time = time.time()
            path, transport_modes_used, total_time, total_cost, transfer_times = minimal_transfer(
                G, "Yeouido", transport_modes, alpha, beta, gamma)
            execution_time = time.time() - start_time

            std_print(path,transport_modes_used,total_time,total_cost,transfer_times,execution_time)
            plot_graph(G, path, transport_modes_used, transfer_times, transport_modes,title_text)

        elif choice == "2":
            title_text = "Fastest Route"
            print("\n--- Fastest Route ---")
            
            start_time=time.time()
            path, transport_modes_used, total_time, total_cost, transfer_times = find_fastest_path(
            G, "Yeouido", transport_modes)  
            execution_time = time.time() - start_time         
            
            std_print(path,transport_modes_used,total_time,total_cost,transfer_times,execution_time)
            plot_graph(G,path,transport_modes_used,transfer_times,transport_modes,title_text)

        elif choice == "3":
            title_text = "Least Cost Travel"
            print("\n--- Least Cost Travel ---")

            start_time = time.time()
            path, transport_modes_used, total_cost,total_time, transfer_times = find_min_cost(G, "Yeouido", transport_modes)
            execution_time = time.time() - start_time
            
            std_print(path,transport_modes_used,total_time,total_cost,transfer_times,execution_time)
            plot_graph(G,path, transport_modes_used, transfer_times, transport_modes,title_text)
        
        elif choice == "4":
            title_text = "All Transports Path"
            print("\n--- All Tranpsorts Path ---")
            
            start_time = time.time()
            path, transport_modes_used, total_cost, total_time, transfer_times = all_transports_path(G, "Yeouido", transport_modes)
            execution_time = time.time() - start_time
            
            std_print(path,transport_modes_used,total_time,total_cost,transfer_times,execution_time)
            plot_graph(G,path, transport_modes_used, transfer_times, transport_modes,title_text)
        

        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
