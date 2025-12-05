from app.graphs.graph_builder import GraphBuilder

class DummyLLM:
    def invoke(self, msg):
        class R:
            content = "dummy"
        return R()

    def with_structured_output(self, _):
        class T:
            def invoke(self, _):
                class R:
                    content = "translated"
                return R()
        return T()

def test_language_graph_routes_english():
    gb = GraphBuilder(DummyLLM())
    graph = gb.setup_graph(usecase="language")
    state = graph.invoke({"topic": "t", "current_language": "english"})
    assert "blog" in state
