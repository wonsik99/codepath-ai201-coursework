# Evaluation Spec — Pod Classifier

Complete this spec **before** writing any code for Milestone 3.

Use Plan or Ask mode to think through each blank field. When you're done,
your answers here become the blueprint for `compute_accuracy()` and
`compute_per_class_accuracy()` in `evaluate.py`.

---

## Background: What is evaluation?

After building a classifier, we need to know how well it works. Evaluation answers:
- **Overall:** What fraction of episodes did we classify correctly?
- **Per-class:** Are we better at some labels than others?

Both functions take the same inputs: a list of predicted labels and a list of
ground-truth labels, in the same order.

---

## compute_accuracy(predictions, ground_truth)

### What it does
Returns the fraction of predictions that exactly match the ground truth.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`, one per episode. |
| `ground_truth` | `list[str]` | The correct labels, in the same order as `predictions`. |

### Output

| Return value | Type | Description |
|---|---|---|
| accuracy | `float` | A value between 0.0 and 1.0. |

---

### Spec fields — fill these in before writing code

**Formula:**

```
Count how many (prediction, ground_truth) pairs match exactly, then divide by
the total number of predictions. A pair is correct when predicted == ground_truth.
accuracy = correct_count / len(predictions)
```

---

**Step-by-step logic:**

```
1. If predictions is empty, return 0.0 (avoid division by zero).
2. Zip predictions and ground_truth together in order.
3. Count pairs where predicted == truth.
4. Return count / len(predictions) as a float between 0.0 and 1.0.
```

---

**Edge case — what if both lists are empty?**

```
Return 0.0. There are no predictions to evaluate, so accuracy is undefined as a
ratio — returning 0.0 is a safe default that avoids a ZeroDivisionError.
```

---

**Worked example:**

```
predictions  = ["interview", "solo", "panel", "interview"]
ground_truth = ["interview", "solo", "solo",  "narrative"]

Pair 0: interview == interview  ✓
Pair 1: solo      == solo       ✓
Pair 2: panel     == solo        ✗
Pair 3: interview == narrative   ✗

correct = 2, total = 4 → compute_accuracy() returns 0.5 (50%)
```

---

## compute_per_class_accuracy(predictions, ground_truth)

### What it does
Returns accuracy broken down by each label. For each label in `VALID_LABELS`,
reports how many episodes with that ground-truth label were classified correctly.

### Inputs

| Parameter | Type | Description |
|---|---|---|
| `predictions` | `list[str]` | Labels predicted by `classify_episode()`. |
| `ground_truth` | `list[str]` | Correct labels, in the same order. |

### Output

A `dict` keyed by label. Each value is a dict with three keys:

```python
{
    "interview": {"correct": int, "total": int, "accuracy": float},
    "solo":      {"correct": int, "total": int, "accuracy": float},
    "panel":     {"correct": int, "total": int, "accuracy": float},
    "narrative": {"correct": int, "total": int, "accuracy": float},
}
```

---

### Spec fields — fill these in before writing code

**What does "correct" mean for a given class?**

```
For the "interview" class: an episode counts as correct when its ground_truth
is "interview" AND the predicted label is also exactly "interview". We only
increment correct for episodes whose true label is that class.
```

---

**What does "total" mean for a given class?**

```
"total" is the number of test episodes whose ground_truth equals that label —
NOT the total number of all predictions. For interview, total = how many
episodes in the test set are truly interview episodes.
```

---

**Step-by-step logic:**

```
1. Initialize a dict for each label in VALID_LABELS with correct=0, total=0, accuracy=0.0.
2. Loop over zip(predictions, ground_truth).
3. For each pair: increment total for the ground_truth label; if predicted == truth,
   also increment correct for that label.
4. After the loop, for each label set accuracy = correct / total (or 0.0 if total == 0).
5. Return the dict keyed by label.
```

---

**Edge case — what if a class has no examples in ground_truth (total == 0)?**

```
Set accuracy to 0.0 for that class. There were no episodes of that label in the
test set, so per-class accuracy is undefined — 0.0 matches the docstring in evaluate.py.
```

---

**Worked example:**

```
predictions  = ["interview", "interview", "solo", "panel", "panel"]
ground_truth = ["interview", "solo",      "solo", "panel", "narrative"]

label       correct  total  accuracy
----------  -------  -----  --------
interview   1        1      1.0
solo        1        2      0.5
panel       1        1      1.0
narrative   0        1      0.0
```

---

## Reflection questions (discuss at the checkpoint)

1. Your overall accuracy might be decent even if one class has very low accuracy.
   Why is per-class accuracy a more informative metric than overall accuracy alone?

2. If `panel` episodes consistently get misclassified as `interview`, what does
   that tell you about your training labels or your prompt?

3. You labeled 20 training episodes and evaluated on 20 test episodes (5 per class).
   How might the evaluation results change if you had labeled 100 training episodes?
   What if you had 200 test episodes?
