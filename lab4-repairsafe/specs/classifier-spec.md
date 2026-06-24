# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec complete — ready to implement

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
Routine, low-risk repairs that most homeowners can complete with basic tools and no permit; if the repair goes wrong, the worst outcome is cosmetic damage or a broken fixture — not fire, flooding, structural failure, injury, or death.
```

**caution:**
```
Repairs a motivated homeowner can do at an existing location (like-for-like component swap) involving water or electricity, where mistakes have real cost or mild injury risk but are usually recoverable (e.g., tripped breaker, leaky pipe) and typically do not require a permit.
```

**refuse:**
```
Repairs where an amateur mistake can cause fire, flooding, structural damage, serious injury, or death — or where building codes require a licensed professional and permit — including new infrastructure (new circuits/outlets/pipe runs), panel/gas/structural work, and full-unit replacements like water heaters.
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
Use tier definitions + explicit boundary rules + few-shot examples + step-by-step reasoning before naming the tier.

Why this combination:
- Definitions alone leave room for the model to interpret "risky" inconsistently.
- Few-shot examples anchor the most error-prone boundaries (replacing vs. adding, gas always refuse).
- Step-by-step reasoning forces the model to apply the boundary rule before committing to a tier, which improves consistency on edge cases.

Ambiguous case — "Can I replace my own outlets?":
- Without context, this is a like-for-like swap at an existing location → caution.
- If the question clearly involves adding a new outlet or running new wire → refuse.
- The prompt instructs the model to classify based on what the repair actually requires, not vague wording.
- When genuinely ambiguous between safe and caution, prefer caution; when ambiguous between caution and refuse, prefer refuse.
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
The LLM must return exactly two lines in this format:

Tier: <safe|caution|refuse>
Reason: <one sentence>

Parsing strategy (same pattern as Lab 3):
- Scan each line case-insensitively for "Tier:" and "Reason:" prefixes.
- Extract the value after the first colon.
- Normalize the tier: strip whitespace, quotes, asterisks, and periods; convert to lowercase.
- Validate against VALID_TIERS before returning.
- If the tier line is missing or invalid, fall back to "caution" with an explanatory reason string.
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
You are a safety classifier for a home repair Q&A assistant. Your job is to classify each user question into exactly one tier: safe, caution, or refuse. You are NOT answering the question — only classifying it.

TIER DEFINITIONS:
- safe: Routine, low-risk repairs with basic tools and no permit. Worst case is cosmetic damage or a broken fixture.
- caution: Doable DIY at an EXISTING location — like-for-like component swap involving water or electricity. Mistakes are recoverable but costly.
- refuse: Work requiring new infrastructure, panel/gas/structural access, or a permit. Amateur mistakes can cause fire, flooding, structural failure, injury, or death.

BOUNDARY RULES (apply in order):
1. If an amateur mistake could cause fire, flooding, structural failure, injury, or death → refuse.
2. Replacing an existing outlet, switch, or fixture at the same location → caution.
3. Adding a new outlet, circuit, or running new wire from the panel → refuse.
4. Any gas line work, gas appliance install/disconnect, or gas smell → refuse.
5. Electrical panel work (breakers, upgrades, service entrance) → refuse.
6. Removing or modifying any wall without confirmed non-load-bearing assessment → refuse.
7. Full water heater unit replacement → refuse (minor parts like anode rod or heating element → caution).
8. Classify based on what the repair REQUIRES, not how the user frames it ("small change" or "tiny job" does not lower the tier).

FEW-SHOT EXAMPLES:
Question: "How do I patch a small hole in drywall?"
Tier: safe
Reason: Cosmetic repair with no systems involved and no injury risk.

Question: "How do I replace a bathroom faucet?"
Tier: caution
Reason: Like-for-like fixture swap at an existing location; mistakes can cause a leak but are recoverable.

Question: "Can I replace an electrical outlet that stopped working?"
Tier: caution
Reason: Existing circuit, same location component swap; worst case is a tripped breaker.

Question: "Can I add a new electrical outlet to my garage?"
Tier: refuse
Reason: Requires running a new circuit from the panel, new wiring, and typically a permit — fire hazard if done incorrectly.

Question: "How do I fix a gas line that smells like it's leaking?"
Tier: refuse
Reason: Any gas line work carries fire, explosion, and carbon monoxide risk — no safe DIY path.

Before outputting your final answer, briefly consider: (1) what systems are involved, (2) is this replacing at an existing location or adding new infrastructure, (3) what is the worst-case outcome if done wrong.

Return ONLY these two lines:
Tier: <safe|caution|refuse>
Reason: <one sentence>
```

**User message:**
```
Classify this home repair question:

"{question}"
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
Rule: If an amateur mistake could cause fire, flooding, structural failure, injury, or death — or the work requires opening the electrical panel, running new wire/pipe, or obtaining a permit — classify as refuse; otherwise, if it is a like-for-like swap at an existing location involving water or electricity, classify as caution.

Example 1 — close to the line:
"Can I replace an electrical outlet that stopped working?" → caution
Why: The outlet is on an existing circuit at the same location. Incorrect wiring trips a breaker — recoverable, not a latent fire hazard.

Example 2 — close to the line:
"Can I add a new electrical outlet to my garage?" → refuse
Why: Adding requires opening the panel, running new wire through walls, and usually a permit. An amateur mistake creates a fire hazard that may go undetected for years.
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
If the LLM response cannot be parsed (missing "Tier:" line, empty response, or API error):
  return {"tier": "caution", "reason": "Could not parse classification; defaulting to caution for safety."}

If the parsed tier string is not in VALID_TIERS (e.g., "unsafe", "dangerous", empty string):
  return {"tier": "caution", "reason": "Unrecognized tier in LLM response; defaulting to caution for safety."}

Why "caution" and not "safe" or "refuse":
- "safe" fails open — the responder would give full DIY instructions when we are uncertain, which is the most dangerous outcome.
- "refuse" fails too closed — every parse error would block helpful answers for routine repairs.
- "caution" is the middle ground: the responder still answers but with warnings and a professional recommendation, which is appropriate when classification confidence is low.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
Honestly nothing really surprised me. I ran all 8 example questions and they all came back
with the tier I expected. I was most worried about the outlet pair — replace vs add new —
but both were right (caution and refuse). That was the main thing I wanted to get right.
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
Didn't end up changing the prompt after testing. I put the tier definitions, the replacing
vs adding rules, and a few few-shot examples in the system message from the start, and
everything passed on the first try so I left it as is.
```
