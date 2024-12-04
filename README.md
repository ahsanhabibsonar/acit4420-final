# Python Pathfinding and File Organizer Project

## Overview

This project is divided into two main components:

1. **Thoughtful Planner**: Implements various pathfinding algorithms (Minimal Transfer, Fastest Route, Least Cost, All Transports Path) to simulate travel routes with multiple transport modes. This module leverages data from CSV files and dynamically visualizes travel paths using graph representations.
   
2. **Dynamic File Organizer**: A utility to organize files in a directory based on their extensions. It can dynamically handle unknown file types by categorizing them and storing the categories in a CSV file.

---

## Features

### Thoughtful Planner

- **Pathfinding Algorithms**:
  - Minimal Transfer using a Greedy Neighbor approach.
  - Fastest Route using Dijkstra's algorithm.
  - Least Cost computation with Dijkstra's algorithm.
  - All Transport Modes simulation with custom logic.

- **Graph Visualization**:
  - Displays nodes and edges with transport-specific coloring.
  - Labels transfer times and distances dynamically.

- **Dynamic User Input**:
  - Add new coordinates interactively with distance validations.

### Dynamic File Organizer
- Categorizes files in a directory based on extensions.
- Logs all file movements and errors for debugging.
- Dynamically handles unknown file types by updating a CSV file.

---


## Project Directory Structure

```plaintext
Project Root
├── address_data.csv           # CSV file with address and coordinate data
├── transport_modes.csv        # CSV file with transport modes and attributes
├── data_loader.py             # Loads and validates data
├── main.py                    # Entry point for both modules
├── graph_builder.py           # Constructs graphs for pathfinding
├── minimal_transfer.py        # Minimal Transfer pathfinding logic
├── fastest_path.py            # Fastest Route pathfinding logic
├── least_cost.py              # Least Cost pathfinding logic
├── all_transport_modes.py     # All Transport Modes pathfinding logic
├── plotting.py                # Graph visualization utility
├── test_project.py            # Unit tests for Thoughtful Planner
├── test_emptyGraph.py         # Unit tests for Thoughtful Planner
├── dynamic_extension.py       # Dynamically handles unknown file extensions
├── logger.py                  # Centralized logging for error handling
├── organizer.py               # File Organizer implementation
├── categories.csv             # CSV file with file type mappings
├── test_file_organizer.py     # Unit tests for File Organizer

```

---

## Installation

1. Clone the repository: git clone https://github.com/ahsanhabibsonar/acit4420-final cd acit4420-final

2. Install dependencies: pip install -r requirements.txt


---

## Usage

### Thoughtful Planner
1. Run the program: python3 main.py

2. Follow the menu options to:
- Add coordinates.
- Run various pathfinding algorithms.
- View the results, including transfer times, paths, and visualized graphs.


### Dynamic File Organizer
1. Run the program: python3 main.py

2. Enter the target directory when prompted.
3. Files will be categorized based on extensions. Unknown file types are dynamically handled.

---

## Testing

Unit tests are provided to ensure functionality:

### Thoughtful Planner
1. Run pytest test_project.py or python3 -m pytest test_project.py
2. It will test data loading, graph building and least cost functionality. Test csv file is available in the repository.

----
1. Run pytest test_emptyGraph.py or python3 -m pytest test_emptyGraph.py
2. It will test Empty Graph situation

### Dynamic File Organizer
1. Run pytest test_file_organizer.py or python3 -m pytest test_file_organizer.py
2. It creates .jgp and .pdf file automatically and then sorts and moved to category folder. 


## Limitations
- Newly added coordinates are not dynamically reflected in the graph visualization.
- Some edge cases in transport mode assignments may produce unexpected results.

---

## Future Improvements
- Add constraints for global maximum time and cost instead of segment-based constraints.
- Improve graph connectivity validation and error handling.
- Enhance performance testing for larger graphs and file sets.

---

## License

This project is licensed under the MIT License.
