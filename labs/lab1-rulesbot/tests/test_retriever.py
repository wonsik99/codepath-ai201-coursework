import retriever


class FakeCollection:
    def __init__(self, count, results=None):
        self._count = count
        self._results = results
        self.query_args = None

    def count(self):
        return self._count

    def query(self, **kwargs):
        self.query_args = kwargs
        return self._results


def test_retrieve_returns_empty_list_for_blank_query(monkeypatch):
    collection = FakeCollection(count=2)
    monkeypatch.setattr(retriever, "_collection", collection)

    assert retriever.retrieve("   ") == []
    assert collection.query_args is None


def test_retrieve_returns_empty_list_for_empty_collection(monkeypatch):
    collection = FakeCollection(count=0)
    monkeypatch.setattr(retriever, "_collection", collection)

    assert retriever.retrieve("How do I win?") == []
    assert collection.query_args is None


def test_retrieve_maps_nested_results_and_orders_by_distance(monkeypatch):
    collection = FakeCollection(
        count=2,
        results={
            "documents": [["Second-best rule", "Best rule"]],
            "metadatas": [[{"game": "Risk"}, {"game": "Catan"}]],
            "distances": [[0.42, 0.11]],
        },
    )
    monkeypatch.setattr(retriever, "_collection", collection)

    matches = retriever.retrieve("How do I win?", n_results=5)

    assert matches == [
        {"text": "Best rule", "game": "Catan", "distance": 0.11},
        {"text": "Second-best rule", "game": "Risk", "distance": 0.42},
    ]
    assert collection.query_args == {
        "query_texts": ["How do I win?"],
        "n_results": 2,
        "include": ["documents", "metadatas", "distances"],
    }
