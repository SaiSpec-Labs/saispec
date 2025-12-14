🛡️ SaiSpec: The AI Governance & Logic Audit SystemSaiSpec is a runtime governance framework for AI Agents. It acts as a "Flight Recorder" and "Safety Interceptor" for LLM-based applications.Unlike simple guardrails that check for bad words, SaiSpec enforces stateful governance protocols:RBAC: Does the agent have the license to use this tool? (AuthorityGuard)Accountability: Did the agent justify its high-stakes decision? (AccountabilityGuard)Impact Control: Is a human watching this irreversible action? (ImpactAwareness)Fairness: Is the logic free from demographic bias? (FairnessGuard)🚀 Quick Start1. InstallBashpip install saispec
2. Define Your PolicyWrap your agent's execution loop with the SaiRecorder.Pythonfrom saispec import SaiRecorder, AgentContext, DecisionClass
from saispec.specs import AuthorityGuard, AccountabilityGuard, ImpactAwareness

# 1. Define Permissions (The License)
permissions = {
    "transfer_funds": ["finance_access"],
    "delete_db": ["admin_root"]
}

# 2. Define Context (The Driver)
ctx = AgentContext(
    user_id="user_123",
    permissions=["finance_access"], # Has finance, but NOT admin
    human_in_loop=False
)

# 3. Run with Governance
with SaiRecorder(specs=[AuthorityGuard(permissions), ImpactAwareness()], context=ctx) as sai:
    
    # ✅ ALLOWED: User has finance_access
    sai.log("tool_call", "transfer_funds", decision_class=DecisionClass.DECISIVE)
    
    # 🛑 BLOCKED: User lacks admin_root
    sai.log("tool_call", "delete_db", decision_class=DecisionClass.IRREVERSIBLE)
🧠 Core Concepts1. Decision ClassesNot all actions are equal. SaiSpec classifies them by risk:INFO: Safe, read-only (e.g., Search).ADVISORY: Recommendations (e.g., Draft Email).DECISIVE: Actions on behalf of user (e.g., Book Flight).IRREVERSIBLE: Destructive actions (e.g., Transfer Money, Delete Data).2. The Audit TrailEvery action is logged to a cryptographically verifiable trace.JSON[
  {
    "timestamp": "2025-12-14T10:00:01",
    "step_type": "tool_call",
    "tool": "transfer_funds",
    "decision_class": "DECISIVE",
    "status": "PASSED"
  },
  {
    "timestamp": "2025-12-14T10:00:05",
    "step_type": "system_audit",
    "content": "SECURITY OVERRIDE: AuthorityGuard DISABLED. Reason: 'Emergency Authorization'",
    "actor": "SYSTEM"
  }
]
🛡️ Available GuardsGuardFunctionWhy use it?AuthorityGuardRole-Based Access ControlPrevents support agents from performing admin tasks.AccountabilityGuardForced Chain-of-ThoughtEnsures high-risk actions are justified by reasoning.ImpactAwarenessHuman-in-the-Loop EnforcerStops irreversible actions if no human is watching.FairnessGuardBias DetectionFlags decisions based on protected attributes.NoLoopsStability CheckPrevents infinite loops and wasted API costs.📦 Installation for DevelopmentBashgit clone https://github.com/saispec-labs/saispec.git
cd saispec
pip install -e .
