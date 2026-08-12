from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)

_FALLBACK = {
    "tier": "caution",
    "reason": "Could not parse classification; defaulting to caution for safety.",
}

_SYSTEM_PROMPT = """You are a safety classifier for a home repair Q&A assistant. Your job is to classify each user question into exactly one tier: safe, caution, or refuse. You are NOT answering the question — only classifying it.

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
Reason: <one sentence>"""


def _parse_tier_response(content: str | None) -> dict:
    """Extract tier and reason from the LLM's text response."""
    if not content or not content.strip():
        return dict(_FALLBACK)

    response_text = content.strip()
    tier = ""
    reason = response_text
    found_tier_line = False

    for line in response_text.splitlines():
        lower_line = line.lower()
        if lower_line.startswith("tier:"):
            raw = line.split(":", 1)[1].strip().lower().strip("*\"'.")
            tier = raw
            found_tier_line = True
        elif lower_line.startswith("reason:"):
            reason = line.split(":", 1)[1].strip()

    if not found_tier_line or tier not in VALID_TIERS:
        return {
            "tier": "caution",
            "reason": "Unrecognized tier in LLM response; defaulting to caution for safety.",
        }

    return {"tier": tier, "reason": reason}


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned
    """
    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f'Classify this home repair question:\n\n"{question}"',
                },
            ],
            max_tokens=200,
            temperature=0,
        )
        content = response.choices[0].message.content
        return _parse_tier_response(content)
    except Exception as e:
        return {
            "tier": "caution",
            "reason": f"API error during classification; defaulting to caution for safety: {e}",
        }
