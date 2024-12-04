def test_empty_graph():
    from minimal_transfer import minimal_transfer
    import networkx as nx

    graph = nx.Graph()  # Empty graph
    transport_modes = {
        "Walking": {"Speed_kmh": 5, "Cost_per_km": 0, "Transfer_Time_min": 0}
    }

    path, modes, time, cost, transfers = minimal_transfer(
        graph, "Nonexistent_Node", transport_modes, 1, 2, 3
    )

    assert path == [], "Path should be empty for an empty graph"
    assert modes == [], "Transport modes should be empty for an empty graph"
    assert time == 0, "Total time should be 0 for an empty graph"
    assert cost == 0, "Total cost should be 0 for an empty graph"
