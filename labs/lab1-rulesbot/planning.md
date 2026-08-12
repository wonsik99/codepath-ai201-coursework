# RulesBot — Planning Doc

Use this file to record your design decisions as you work through the lab.
There are no wrong answers — write enough that you could explain your reasoning to another group.

---

## Chunking Strategy

**Chunk size:**

300 characters. This generally keeps one short rule together without combining
too many unrelated rules.

**Overlap:**

50 characters, so a sentence crossing a window boundary remains represented in
the next chunk.

**Why this strategy fits rule book text:**

Rules are short and semantically dense. A fixed sliding window gives predictable
embedding sizes, while the overlap reduces the cost of splitting without adding
a sentence parser. Across all eight books it produced 149 chunks.

---

## Retrieval Observations

After implementing retrieval, try these test queries and record what comes back:

| Query | Top result game | Does it make sense? |
|-------|----------------|---------------------|
| "How do you win?" | Monopoly (0.5072) | Yes; it retrieved the winning condition, but the question is ambiguous across games. |
| "What happens when you roll a 7?" | Catan (0.4664) | Yes; the top chunk contains the `ROLLING A 7` rule. |
| "Can two players share a route?" | Ticket To Ride (0.3653) | Yes; the top result explains double routes. |

**Anything surprising?**

The generic winning query returned Monopoly, Risk, and Ticket To Ride within
`0.0152` distance of one another. The embedding search was behaving correctly;
the question itself needed a game name. A strict `0.5` cutoff also rejected the
correct Monopoly result, so the final response threshold is `0.55`.

---

## Response Quality

After implementing generation, try 2–3 questions and assess the answers:

| Query | Answer accurate? | Properly grounded? | Cited the right game? |
|-------|-----------------|-------------------|----------------------|
| "What happens when you roll a 7 in Catan?" | Yes (live Groq response) | Yes | Yes, `[Catan]` |
| Unknown rule with only weak matches | Yes; returned fallback | Yes | Not applicable |

**What would you change about the prompt to improve grounding?**

Retrieved text is explicitly described as reference material rather than
instructions, and every claim must cite a game in square brackets. Weak chunks
are removed before the API call. The request-building and fallback paths are
covered by automated tests, and the full retrieval-to-Groq path was verified
with a temporary API key that was not saved in the repository.
