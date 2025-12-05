from app.nodes.blog_node import BlogNode

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

def test_translation_preserves_title():
    node = BlogNode(DummyLLM())
    state = {"topic": "t", "blog": {"title": "Title", "content": "Body"}, "current_language": "french"}
    out = node.translation(state)
    assert out["blog"]["title"] == "Title"
    assert out["blog"]["content"] == "translated"
