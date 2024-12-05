#test_project.py
import pytest

from thoughtfulPlanner.data_loader import add_coordinates, load_streets
from thoughtfulPlanner.minimal_transfer import minimal_transfer
from thoughtfulPlanner.graph_builder import build_graph

# Test load_streets
def test_load_streets():
    streets = load_streets("test_address_data.csv")
    assert isinstance(streets, dict)
    assert len(streets) > 0

# Test build_graph
def test_build_graph():
    streets = load_streets("test_address_data.csv")
    graph = build_graph(streets)
    assert len(graph.nodes) > 0
    assert len(graph.edges) > 0


# Test minimal_transfer
def test_minimal_transfer():
    streets = load_streets("test_address_data.csv")
    graph = build_graph(streets)
    #Test_Node = (37.526, 126.929)
    streets["Test_Node"] = (37.526, 126.929)
    transport_modes = {
     'Walking': {'Speed_kmh': 5.0, 'Cost_per_km': 0.0, 'Transfer_Time_min': 0, 'Color': 'red'}
     }

    path, modes, time, cost, transfers = minimal_transfer(graph, "Test_Node", transport_modes, 1, 2, 3)
    
    
    assert isinstance(path, list), "Path should be a list"
    assert len(path) > 0, "Path should not be empty"
    assert time > 0, "Time should be greater than 0"
    assert cost >= 0, "Cost should not be negative"
