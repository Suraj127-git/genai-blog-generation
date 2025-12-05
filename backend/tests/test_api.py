from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_blog_generation_topic_only(monkeypatch):
    class DummyLLM:
        def invoke(self, msg):
            class R:
                content = "dummy"
            return R()

        def with_structured_output(self, _):
            return self

    from app.services.llm_factory import LLMFactory

    def fake_create(provider=None, model=None):
        return DummyLLM()

    monkeypatch.setattr(LLMFactory, "create", staticmethod(fake_create))

    r = client.post("/blogs", json={"topic": "Test"})
    assert r.status_code == 200
    data = r.json()["data"]
    assert "blog" in data

def test_blog_generation_with_language(monkeypatch):
    class DummyLLM:
        def invoke(self, msg):
            class R:
                content = "title or content"
            return R()

        def with_structured_output(self, _):
            class T:
                def invoke(self, _):
                    class R:
                        content = "translated"
                    return R()
            return T()

    from app.services.llm_factory import LLMFactory

    def fake_create(provider=None, model=None):
        return DummyLLM()

    monkeypatch.setattr(LLMFactory, "create", staticmethod(fake_create))

    r = client.post("/blogs", json={"topic": "Test", "language": "english"})
    assert r.status_code == 200
    data = r.json()["data"]
    assert "blog" in data
