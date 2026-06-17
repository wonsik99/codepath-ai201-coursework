import json
import os
from config import (
    LLM_PROVIDER,
    GROQ_API_KEY,
    OPENAI_API_KEY,
    LLM_MODEL,
    VALID_LABELS,
    DATA_PATH,
    TRAIN_FILE,
    LABELS_FILE,
)


def _create_llm_client():
    if LLM_PROVIDER == "openai":
        from openai import OpenAI

        return OpenAI(api_key=OPENAI_API_KEY)

    from groq import Groq

    return Groq(api_key=GROQ_API_KEY)


_client = _create_llm_client()


def load_labeled_examples() -> list[dict]:
    """
    Load the training episodes and merge them with the student's labels.

    Returns a list of dicts, each with:
      - "id"          : episode ID
      - "title"       : episode title
      - "podcast"     : podcast name
      - "description" : episode description
      - "label"       : the label from my_labels.json (may be None if not yet annotated)

    Only returns episodes where the label is a valid, non-null string.
    Episodes with null labels are silently skipped.
    """
    train_path = os.path.join(DATA_PATH, TRAIN_FILE)
    labels_path = os.path.join(DATA_PATH, LABELS_FILE)

    with open(train_path, encoding="utf-8") as f:
        episodes = {ep["id"]: ep for ep in json.load(f)}

    with open(labels_path, encoding="utf-8") as f:
        labels = {entry["id"]: entry["label"] for entry in json.load(f)}

    labeled = []
    for ep_id, ep in episodes.items():
        label = labels.get(ep_id)
        if label in VALID_LABELS:
            labeled.append({**ep, "label": label})

    return labeled


def build_few_shot_prompt(labeled_examples: list[dict], description: str) -> str:
    """
    Build a few-shot classification prompt using the student's labeled training examples.
    """
    task_instruction = """You are classifying podcast episodes by their format. Classify the episode
into exactly one of these four labels:

- interview: a conversation between a host and one or more guests
- solo: a single host speaking from memory, experience, or opinion — no guests,
  no assembled external sources
- panel: multiple guests with roughly equal speaking time, often debating or
  discussing a topic together
- narrative: a story assembled from external sources — interviews, archival
  audio, reporting — with a clear narrative arc

Return only the label and your reasoning. Do not explain the taxonomy."""

    parts = [task_instruction, ""]

    if labeled_examples:
        parts.append("Here are labeled examples:")
        parts.append("")
        for example in labeled_examples:
            parts.extend([
                f"Title: {example['title']}",
                f"Description: {example['description']}",
                f"Label: {example['label']}",
                "---",
                "",
            ])
    else:
        parts.extend([
            "No training examples are available — classify using the label definitions only.",
            "",
        ])

    parts.extend([
        "Classify this new episode. Classify based on whatever text is available.",
        "",
        f"Description: {description}",
        "Label: ?",
        "",
        "Classify the episode above. Return your answer in exactly this format:",
        "Label: <one of interview, solo, panel, narrative>",
        "Reasoning: <1-2 sentences explaining the choice>",
    ])

    return "\n".join(parts)


def _parse_classification_response(content: str | None) -> dict:
    """Extract label and reasoning from the LLM's text response."""
    if not content or not content.strip():
        return {
            "label": "unknown",
            "reasoning": "Empty response from LLM",
        }

    response_text = content.strip()
    label = "unknown"
    reasoning = response_text
    found_label_line = False

    for line in response_text.splitlines():
        lower_line = line.lower()
        if lower_line.startswith("label:"):
            raw = line.split(":", 1)[1].strip().lower()
            raw = raw.strip("*\"'.")
            label = raw
            found_label_line = True
        elif lower_line.startswith("reasoning:"):
            reasoning = line.split(":", 1)[1].strip()

    if label not in VALID_LABELS:
        label = "unknown"

    if not found_label_line:
        reasoning = response_text

    return {"label": label, "reasoning": reasoning}


def _chat_completion_kwargs(prompt: str) -> dict:
    kwargs = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    if LLM_PROVIDER == "openai":
        kwargs["max_completion_tokens"] = 250
    else:
        kwargs["max_tokens"] = 250
    return kwargs


def classify_episode(description: str, labeled_examples: list[dict]) -> dict:
    """
    Classify a single podcast episode description using the few-shot LLM classifier.
    """
    try:
        prompt = build_few_shot_prompt(labeled_examples, description)
        response = _client.chat.completions.create(**_chat_completion_kwargs(prompt))
        content = response.choices[0].message.content
        return _parse_classification_response(content)
    except Exception as e:
        return {
            "label": "unknown",
            "reasoning": f"API error: {e}",
        }
