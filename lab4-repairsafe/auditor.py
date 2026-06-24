import json
import os
from datetime import datetime, timezone

from config import LOG_FILE

QUESTION_MAX_LEN = 300
RESPONSE_PREVIEW_MAX_LEN = 200


def log_interaction(question: str, tier: str, response: str) -> None:
    """
    Append a structured record of this interaction to the audit log.

    Each record is one JSON object on a single line in logs/audit.jsonl (JSONL format).
    """
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    question_truncated = len(question) > QUESTION_MAX_LEN
    logged_question = question[:QUESTION_MAX_LEN]
    response_preview = response[:RESPONSE_PREVIEW_MAX_LEN]

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tier": tier,
        "question": logged_question,
        "response_preview": response_preview,
        "question_length": len(question),
        "response_length": len(response),
        "question_truncated": question_truncated,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    preview = logged_question if len(logged_question) <= 60 else logged_question[:57] + "..."
    print(f'[LOGGED] tier={tier} | "{preview}" → {len(response)} chars')
