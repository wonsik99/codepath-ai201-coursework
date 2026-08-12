from types import SimpleNamespace

import pytest

import generator


class FakeCompletions:
    def __init__(self, content):
        self.content = content
        self.request = None

    def create(self, **kwargs):
        self.request = kwargs
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))]
        )


def make_client(content="You move the robber. [Catan]"):
    completions = FakeCompletions(content)
    client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
    return client, completions


def test_generate_response_falls_back_without_chunks():
    assert (
        generator.generate_response("Unknown rule?", []) == generator.FALLBACK_MESSAGE
    )


def test_generate_response_filters_weak_matches(monkeypatch):
    client, completions = make_client()
    monkeypatch.setattr(generator, "_client", client)
    chunks = [{"text": "Unrelated text", "game": "Risk", "distance": 0.8}]

    assert (
        generator.generate_response("Unknown rule?", chunks)
        == generator.FALLBACK_MESSAGE
    )
    assert completions.request is None


def test_generate_response_builds_grounded_cited_request(monkeypatch):
    client, completions = make_client()
    monkeypatch.setattr(generator, "_client", client)
    chunks = [
        {
            "text": "When a 7 is rolled, move the robber.",
            "game": "Catan",
            "distance": 0.52,
        },
        {"text": "Weak unrelated rule", "game": "Risk", "distance": 0.56},
    ]

    answer = generator.generate_response("What happens when I roll a 7?", chunks)

    assert answer == "You move the robber. [Catan]"
    assert completions.request["model"] == generator.LLM_MODEL
    assert completions.request["temperature"] == 0.0
    system_message, user_message = completions.request["messages"]
    assert "using only the provided rule-book context" in system_message["content"]
    assert "[Catan]" in system_message["content"]
    assert "[Source 1 | Game: Catan]" in user_message["content"]
    assert "Weak unrelated rule" not in user_message["content"]


def test_generate_response_requires_api_key_for_relevant_context(monkeypatch):
    monkeypatch.setattr(generator, "_client", None)
    monkeypatch.setattr(generator, "GROQ_API_KEY", None)
    chunks = [{"text": "A relevant rule", "game": "Uno", "distance": 0.1}]

    with pytest.raises(RuntimeError, match="GROQ_API_KEY is not configured"):
        generator.generate_response("What is the rule?", chunks)
