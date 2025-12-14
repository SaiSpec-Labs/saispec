# 🛡️ SaiSpec

**SaiSpec** is a governance-first runtime framework for AI agents.

It acts as a **flight recorder, policy engine, and safety interceptor** for LLM-driven systems — enforcing *permissions, accountability, and human oversight* at runtime.

Unlike simple guardrails that only scan text, SaiSpec governs **what an agent is allowed to do**, **why it is doing it**, and **who approved it**.

---

## Why SaiSpec?

Modern AI agents don’t just generate text — they:
- call tools
- trigger workflows
- move money
- delete data
- act on behalf of users

SaiSpec answers a critical question:

> **“Does this agent have the authority and justification to take this action?”**

---

## Core Capabilities

- **🔍 Full Traceability**
  - Records every thought, tool call, override, and system intervention
  - Produces audit-ready session reports

- **🔐 Permission & Authority Enforcement**
  - Role-based access control for tools
  - Prevents unauthorized actions at runtime

- **🧠 Accountability Checks**
  - Requires justification for high-risk decisions
  - Blocks actions taken without reasoning

- **🛑 Human-in-the-Loop Controls**
  - Forces human approval for irreversible actions
  - Supports mixed human + AI execution

- **📊 Governance Scoring**
  - Produces a session score based on policy violations
  - Enables automated pass/fail decisions

---

## Installation

```bash
pip install saispec
