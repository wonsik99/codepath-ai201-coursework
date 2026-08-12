# Plant Advisor — AI201 Lab 2

A conversational agent that helps users care for their houseplants. Ask it anything about a plant in its database and it will look up the care requirements, check the current seasonal context, and give you specific, grounded advice.

Built with **Groq** (LLM + tool calling) and **Gradio** (chat UI).

---

## What I Built

The starter shipped with a working UI and data, but two pieces were left unimplemented. I completed both:

### Milestone 1 — `lookup_plant()` (`tools.py`)
Case-insensitive plant search that resolves a name three ways, in order:
1. **Direct key** match (e.g. `"pothos"`)
2. **Display name** match (e.g. `"Pothos"`)
3. **Alias** match (e.g. `"devil's ivy"` → pothos)

Input is lowercased and whitespace-stripped. On a miss it returns a structured
`{"found": False, ...}` result with a helpful message the agent can relay to the user.

### Milestone 2 — `run_agent()` agent loop (`agent.py`)
The full tool-calling loop:
1. Builds the message list: system prompt → conversation history → new user message
2. Calls the Groq LLM with the tool definitions (`tool_choice="auto"`)
3. While the model requests tools: appends the assistant message, runs each call via
   `dispatch_tool()`, and appends results as `role="tool"` messages with their `tool_call_id`
4. Repeats up to `MAX_TOOL_ROUNDS`, then returns the final text answer

The history parser also handles three Gradio message formats (dicts, objects, and
`[user, assistant]` pairs) so it stays compatible across Gradio versions.

---

## Setup

**1. Fork and clone this repo.**

**2. Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Add your Groq API key.** Copy `.env.example` to `.env` and paste in your key from [console.groq.com](https://console.groq.com).

**5. Run the app:**

```bash
python app.py
```

Plant Advisor will open in your browser with the completed tool-calling agent.

---

## Project Structure

```
ai201-lab2-plantadvisor-starter/
├── app.py              ← Gradio UI (complete — do not modify)
├── config.py           ← API keys and settings (complete)
├── agent.py            ← Tool definitions + run_agent() agent loop (implemented)
├── tools.py            ← lookup_plant() + get_seasonal_conditions() (implemented)
├── data/
│   ├── plants.json     ← 15-plant database (complete)
│   └── seasons.json    ← Seasonal care data (complete)
├── specs/
│   ├── system-design.md        ← Start here
│   ├── tool-functions-spec.md  ← Complete before Milestone 1
│   └── agent-loop-spec.md      ← Complete before Milestone 2
└── requirements.txt
```

## Where to Start

Open `specs/system-design.md`. Read the whole thing before opening any code file.
