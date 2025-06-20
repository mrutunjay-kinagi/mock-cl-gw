# ClaimLens + Guidewire ClaimCenter (Art of the Possible Demo using MCP)

This mock project demonstrates a conceptual "Art of the Possible" integration between **Doclens.ai's ClaimLens** and **Guidewire ClaimCenter** using:

* Agentic AI Chat Interface (Streamlit)
* Model context orchestration layer (MCP)
* Simulated ClaimCenter and ClaimLens REST APIs
* Fully Dockerized setup for easy local or cloud demo

---

## Project Modules

```
mock-cl-gw/
├── claimcenter_api/         # Mock Guidewire ClaimCenter API
├── claimlens_api/           # Mock AI analysis engine
├── mcp/                     # MCP logic layer for orchestration
├── agentic_chat_ui/         # Streamlit app for interactive agentic chat
├── docker-compose.yml       # Combined service launcher
└── README.md
```

---

## Agentic Chat Flow

1. User enters a goal into the chat UI (e.g., “Analyze claim C12345 and summarize documents”)
2. MCP interprets the prompt and orchestrates:

   * ClaimCenter API calls: fetch documents, injuries, policy
   * ClaimLens: analyze claim content
3. Chat UI displays structured summary with key findings

---

## Running the Full Demo (Docker)

### 1. Build All Services

```bash
docker-compose build
```

### 2. Launch All Services

```bash
docker-compose up
```

### 3. Open Agentic Chat UI

Visit: [http://localhost:8501](http://localhost:8501)
Use: `claim_id = claim_1` or `claim_2`

---

## Sample Questions to Try

* “Fetch policy details related to this claim”
* “What are the coverages on this policy?”
* “What endorsements apply here?”
* “What are the reported injuries?”
* “Analyze all documents on this claim”

Each prompt is routed by MCP to the appropriate mock services and composed back into a response.

---

## Service Overview

| Service           | Description                            | Port |
| ----------------- | -------------------------------------- | ---- |
| `claimcenter-api` | Simulated Guidewire ClaimCenter APIs   | 8080 |
| `claimlens-api`   | Simulated AI engine for claim analysis | 5001 |
| `mcp`             | Orchestration layer (MCP logic)        | 8002 |
| `chat-ui`         | Streamlit frontend for agentic prompt  | 8501 |

---

## ClaimCenter Mock Data

The `claimcenter_api/data/` folder includes:

* `claims.json`: claim\_1 (Auto), claim\_2 (GL)
* `policies.json`: with policyholder & LOB
* `documents.json`: medical, police, incident reports
* `injuries.json`: body parts + severity
* `coverages.json`: by policy
* `endorsements.json`: by policy

---

## Disclaimer

This is a **proof-of-concept** project. It simulates how ClaimLens could interact with Guidewire ClaimCenter using MCP and agentic AI. This is **not production-ready** and is intended solely to demonstrate the art of the possible.

---

## Credits
Inspired by ClaimLens vision at [Doclens.ai](https://www.doclens.ai)
