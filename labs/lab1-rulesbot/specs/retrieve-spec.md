# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Complete

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

`_collection.query()` receives the stripped question in a one-item
`query_texts` list, the smaller of `n_results` and the collection size, and
`["documents", "metadatas", "distances"]` in `include`. Requesting these three
fields provides the rule text, its game label, and its ranking score without
fetching unused embeddings.

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```python
{
    "text": "When a 7 is rolled, no resources are produced...",
    "game": "Catan",
    "distance": 0.4664,
}
```

`text` comes from `documents`, `game` from the corresponding metadata dict,
and `distance` from the corresponding cosine-distance result.

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

ChromaDB accepts a batch of queries, so every returned field has one outer
list per query. RulesBot sends exactly one query and reads index `[0]` from
`documents`, `metadatas`, and `distances` before zipping the inner lists.

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

`retrieve()` returns all requested matches and leaves thresholding to the
generator. This keeps retrieval reusable for debugging and makes its output
contract predictable. `generate_response()` excludes distances above `0.55`,
which prevents weak context from reaching the LLM while retaining the observed
relevant Monopoly result at `0.5072`.

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

An empty collection, blank query, or non-positive result count returns `[]`
without running an embedding query. Weak matches are returned with their
distances so the generator can reject them. Matches from multiple games remain
ranked together; the generator labels each context section with its game so an
ambiguous question can be answered with explicit sources or declined.

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: What happens when you roll a 7?
Top result game: Catan
Distance score: 0.4664
Does it make sense? Yes. The chunk begins with Catan's ROLLING A 7 rule.
```

**One thing about the query results that surprised you:**

The broad query "How do you win?" returned valid winning-condition chunks from
several games with very similar scores. Adding the game name is important when
the same intent exists in every rule book.
