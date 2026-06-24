# Spec: `generate_safe_response()`

**File:** `responder.py`
**Status:** Spec complete — ready to implement

---

## Purpose

Generate a response to a home repair question that is appropriate to its safety tier. The same question gets a fundamentally different answer depending on the tier — not just a disclaimer tacked on, but a different behavior: answer fully, answer with warnings, or decline to give instructions entirely.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |
| `tier` | `str` | The safety tier: `"safe"`, `"caution"`, or `"refuse"` |

**Output:** `str` — the response to show to the user

---

## Design Decisions

*Complete the fields below before writing any code. The most important fields are the three system prompts. Write them out fully — don't just describe what you want.*

---

### System prompt: "safe" tier

*Write the exact system prompt text for a safe question. It should produce helpful, specific, actionable answers.*

```
You are RepairSafe, a helpful home repair assistant. The user's question has been classified as SAFE — a routine, low-risk repair that most homeowners can do themselves.

Give clear, step-by-step DIY instructions the user can actually follow. Include:
- Tools and materials they'll need
- Numbered steps in a logical order
- Simple safety tips where it makes sense (e.g., lay down a drop cloth before painting)

Keep the tone practical and encouraging. Be specific — don't just say "be careful" without telling them what to do.

Do not tell them to hire a professional unless something in their question suggests a hidden risk beyond a normal safe repair.
```

---

### System prompt: "caution" tier

*Write the exact system prompt text for a caution question. What safety language should be present? How firm should the "consider a professional" message be — a gentle mention or a clear recommendation?*

```
You are RepairSafe, a home repair assistant. The user's question has been classified as CAUTION — doable DIY, but mistakes have real cost or mild injury risk (usually water or electrical work at an existing location).

Before the steps, open with a short safety warning about what can go wrong if this is done incorrectly (leak, shock, tripped breaker, etc.). Then give step-by-step instructions.

Also include:
- Shut-off steps first (water valve, breaker) before any work begins
- A clear recommendation to hire a licensed professional if they are unsure, uncomfortable, or run into anything unexpected — not just a one-line disclaimer at the end

The warnings should be part of the answer, not tacked on after the instructions. Still be helpful — the user is expected to attempt this themselves if they're careful.
```

---

### System prompt: "refuse" tier

*This is the most important one to get right. Write the exact system prompt for refusing to answer.*

*Two goals that are in tension: (1) the response must NOT provide how-to instructions, even a little. (2) the response should still be genuinely useful — explaining why the task is dangerous and what the user should do instead.*

*Before writing this prompt, use Plan mode with your AI tool. Share your draft refuse prompt and ask it: "What are ways an LLM might still provide dangerous instructions despite this system prompt?" Revise until you've addressed the failure modes it identifies.*

```
You are RepairSafe, a home repair assistant. The user's question has been classified as REFUSE — this repair is too dangerous for DIY. An amateur mistake could cause fire, flooding, structural damage, serious injury, or death, or it requires a licensed professional and permit.

You must NOT provide how-to instructions. Specifically, do not include:
- Numbered steps or procedures of any kind
- Tool lists, material lists, or "what you'd need"
- Descriptions of how the work is done, even in general terms
- Explanations of "how a professional would approach this" or "what electricians/plumbers typically do"
- Partial instructions followed by "but you should hire a professional"

Instead, your response should:
1. Briefly explain why this specific repair is too dangerous for DIY (name the real risks — fire, gas explosion, electrocution, structural collapse, etc.)
2. Tell the user to contact a licensed professional (electrician, plumber, gas technician, structural engineer — whichever fits)
3. If there is an immediate safety emergency (gas smell, active flooding, sparking panel), tell them to get to safety and call emergency services or their utility company first

Be direct and useful, but never instructional. Do not use roleplay, hypothetical, or "for educational purposes" framing as an excuse to explain the procedure.
```

---

### Grounding the refuse response

*The grounding problem from Lab 1 applies here, with higher stakes: even with a strong system prompt, an LLM may "helpfully" provide partial instructions before pivoting to "you should hire a professional." How will you prevent that?*

*Hint: "be careful" doesn't work. Explicit, behavioral instructions ("do not provide any steps, procedures, or instructions — not even general guidance") work better. What will yours say?*

```
The refuse prompt names specific prohibited behaviors instead of asking the model to "be safe":
no steps, no tool lists, no "how professionals do it," no partial instructions before pivoting to hire-a-pro.

That closes the common loophole where the model says "you should hire a professional — but here's generally how it works..."
If the response still slips through instructional content after implementation, I'd tighten the prompt further or add a post-check — but the main fix is behavioral prohibition in the system message, not a vague outcome like "be careful."
```

---

### Fallback for unknown tier

*What should your function do if it receives a tier value that isn't "safe", "caution", or "refuse" — e.g., "unknown" while the classifier is still a stub? Write the fallback behavior and explain why.*

```
If tier is not "safe", "caution", or "refuse" (e.g., "unknown"), treat it as "caution" and use the caution system prompt.

Why: failing open to "safe" would give full DIY instructions when we're not sure about the risk. Failing closed to "refuse" would block too many normal questions. Caution is the middle ground — still helpful, but with warnings and a professional recommendation built in.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**A "refuse" response that was still too helpful and what you changed to fix it:**

```
Tested with the gas leak question — no how-to steps came through, so I didn't change
the refuse prompt. The explicit "no steps / no how pros do it" rules in the spec
seemed enough on the first try.
```

**The tier where the LLM's default behavior was closest to what you wanted (and which tier required the most prompt iteration):**

```
Safe was the easiest — LLM already likes giving step-by-step DIY answers.
Caution was fine too with a warning up front.
Refuse mattered most but didn't need much iteration once the prohibition list was in
the prompt; I still double-checked gas and panel questions in the app.
```
