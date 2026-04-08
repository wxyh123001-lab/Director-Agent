from graph import build_graph

def test_graph_builds_without_error():
    graph = build_graph()
    assert graph is not None

def test_graph_has_correct_nodes():
    graph = build_graph()
    assert hasattr(graph, "invoke")
