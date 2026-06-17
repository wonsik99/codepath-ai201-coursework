# Classifier Spec — Pod Classifier

Complete this spec **before** writing any code for Milestone 2.

Use Plan or Ask mode to think through each blank field. When you're done,
your answers here become the blueprint for `build_few_shot_prompt()` and
`classify_episode()` in `classifier.py`.

---

## build_few_shot_prompt(labeled_examples, description)

### What it does
Constructs a prompt string for the LLM that includes the task instructions,
all labeled training examples, and the new episode description to classify.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `labeled_examples` | `list[dict]` | Each dict has `"title"`, `"description"`, `"label"` (and others). These are the examples you labeled in Milestone 1. |
| `description` | `str` | The episode description to classify. |

### Output

| Return value | Type | Description |
|---|---|---|
| prompt | `str` | A complete prompt string ready to send to the LLM. |

---

### Spec fields — fill these in before writing code

**Task instruction (what should the LLM know about the task?):**

```
You are classifying podcast episodes by their format. Classify the episode
into exactly one of these four labels:

- interview: a conversation between a host and one or more guests
- solo: a single host speaking from memory, experience, or opinion — no guests,
  no assembled external sources
- panel: multiple guests with roughly equal speaking time, often debating or
  discussing a topic together
- narrative: a story assembled from external sources — interviews, archival
  audio, reporting — with a clear narrative arc

Return only the label and your reasoning. Do not explain the taxonomy.
```

---

**How should labeled examples be formatted in the prompt?**

```
Each example should include the episode title, a brief excerpt or the full
description, and the correct label. Separate examples with a blank line or
a delimiter like "---". Include all fields that help the model see why the
label was applied — title and description are both useful; other fields
(like episode ID) are not needed.
```

---

**Example block sketch (write one concrete example):**

```
Title: {title}
Description: {description}
Label: {label}
```

---

**How should the new episode (to be classified) be presented?**

```
Present it in the same format as the labeled examples, but omit the Label
line and replace it with an instruction to classify. For example:

Title: {title}
Description: {description}
Label: ?

Then add a line like: "Classify the episode above. Return your answer in
the format below:" followed by the output format you chose.
```

---

**What output format should you request from the LLM?**

```
Use a fixed two-line text format (not JSON):

Label: <one of interview, solo, panel, narrative>
Reasoning: <1-2 sentences explaining the choice>

Tradeoffs:
- "Label: X / Reasoning: Y" is easy to parse with simple string splits and
  handles capitalization or markdown (**interview**) with strip/lower cleanup.
- JSON looks structured but often breaks on quotes, newlines, or trailing commas.
- A label-only line is simplest to parse but gives no reasoning for the UI.

The prompt will end with: "Return your answer in exactly this format:" followed
by the two lines above as a template.
```

---

**Edge cases to handle in the prompt:**

```
- labeled_examples is empty: still include the task instruction and taxonomy,
  but add a note like "No training examples are available — classify using the
  label definitions only." Skip the examples block entirely.
- description is very short: include it as-is under Description: and add
  "Classify based on whatever text is available."
- New episode has no title (classify_episode only receives description): use
  Description: {description} and Label: ? without a Title line, or use
  Title: (not provided).
```

---

## classify_episode(description, labeled_examples)

### What it does
Classifies a single podcast episode description using the few-shot LLM classifier.
Returns a dict with a label and reasoning.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `description` | `str` | The episode description to classify. |
| `labeled_examples` | `list[dict]` | Labeled training examples from `load_labeled_examples()`. |

### Output

| Return value | Type | Description |
|---|---|---|
| result | `dict` | Must have keys `"label"` and `"reasoning"`. `"label"` must be one of `VALID_LABELS` or `"unknown"`. |

---

### Spec fields — fill these in before writing code

**Step 1 — Build the prompt:**

```
Call build_few_shot_prompt(labeled_examples, description) and store the
returned string in a variable (e.g., prompt). Pass through both arguments
exactly as received — no modification needed before calling.
```

---

**Step 2 — Send to the LLM:**

```
Call _client.chat.completions.create() with:
  - model: LLM_MODEL from config.py ("llama-3.3-70b-versatile")
  - messages: a list with one dict — {"role": "user", "content": prompt}
  - max_tokens: 250 to keep responses concise

Extract the response text from:
  response.choices[0].message.content
```

---

**Step 3 — Parse the response:**

```
1. response_text = content.strip() if content else ""
2. Initialize label = "unknown" and reasoning = response_text (fallback).
3. Loop over response_text.splitlines():
   - If line.lower().startswith("label:"):
     raw = line.split(":", 1)[1].strip().lower()
     raw = raw.strip("*\"'.")   # handle **interview** or "interview".
     label = raw
   - If line.lower().startswith("reasoning:"):
     reasoning = line.split(":", 1)[1].strip()
4. If no Label: line was found, keep label as "unknown" and put the full
   response in reasoning so debugging is possible.
```

---

**Step 4 — Validate the label:**

```
After parsing, check: if label not in VALID_LABELS, set label = "unknown".
Keep the reasoning text as-is so the UI still shows why the model answered
that way. VALID_LABELS = ["interview", "solo", "panel", "narrative"].
```

---

**Step 5 — Handle errors gracefully:**

```
Wrap the API call and parsing in try/except.

What can go wrong:
- Groq API error (network, rate limit, invalid key) → return
  {"label": "unknown", "reasoning": "API error: <message>"}
- Empty or null response content → return
  {"label": "unknown", "reasoning": "Empty response from LLM"}
- Unparseable format (no Label: line, or garbage text) → label stays
  "unknown"; reasoning contains the raw response for debugging

Never raise an exception to the caller — Milestone 3 calls this 20 times in
a loop and one failure must not crash the whole evaluation run.
```

---

### Return value structure

```python
{
    "label": str,      # one of VALID_LABELS, or "unknown" if invalid/error
    "reasoning": str,  # brief explanation from the LLM
}
```

---

## Notes on label quality

The classifier is only as good as your labels. If your training examples have
inconsistent or ambiguous labels, the LLM will learn the wrong pattern.

Before implementing the classifier, re-read `data/taxonomy.md` and double-check
any labels you're unsure about. Annotation quality is part of the lab.

---

## Implementation Notes

*Fill this in after implementing and testing both functions.*

**Test: what does the raw LLM response look like for one episode?**

```
Episode tested: The Case for Four-Day Workweeks
Raw response text:
Label: solo
Reasoning: The episode features a single host sharing their thoughts and opinions on a topic, with no mention of guests or external sources being assembled into a narrative.
```

**How did you parse the label out of the response?**

```
Loop over splitlines(). For lines starting with "label:" (case-insensitive),
take text after the first colon, strip whitespace, lower(), then strip markdown
quotes and asterisks with strip("*\"'.") . Compare result to VALID_LABELS.
Lines starting with "reasoning:" populate the reasoning field the same way.
```

**Did any episodes return `"unknown"`? If so, why?**

```
No on the four UI smoke tests (solo, interview, narrative, panel). Unit tests
still return "unknown" for invalid label strings and empty responses as expected.
```

**One thing about the output format that surprised you:**

```
The model followed the Label:/Reasoning: format reliably on the first try.
The parser still handles markdown variants like "Label: **solo**" via strip("*\"'.").
```
