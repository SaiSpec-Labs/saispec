import time
from saispec import (
    SaiRecorder, AgentContext, DecisionClass, Severity, StepType,
    AuthorityGuard, AccountabilityGuard, ImpactAwareness, NoLoops,
    GovernanceError, FatalSecurityError
)

# SETUP
tool_permissions = {
    "transfer_funds": ["finance_access"], 
    "delete_account": ["admin_root"],
    "refund_user": ["support_lead"]
}

context = AgentContext(
    user_id="user_123",
    permissions=["support_lead", "finance_access"], 
    has_user_consent=True,
    human_in_loop=False
)

specs = [
    AuthorityGuard(tool_permissions),
    AccountabilityGuard(min_thought_length=10),
    ImpactAwareness(),
    NoLoops(max_retries=2)
]

print("\n🛡️  SAISPEC GOVERNANCE SYSTEM | INITIALIZING...")
print(f"👤 User Context: {context.user_id} | Perms: {context.permissions}")
print("-" * 60)

try:
    with SaiRecorder(specs=specs, context=context) as sai:
        
        # Scenario 1: Success
        print("\n[Scenario 1] Valid Refund Request...")
        sai.log(StepType.THOUGHT, "User requested a refund. I have verified the transaction.")
        sai.log(StepType.TOOL_CALL, "refund_user", tool_name="refund_user", decision_class=DecisionClass.DECISIVE)
        print("   ✅ Action Allowed.")

        # Scenario 2: Blocked (No Thought)
        print("\n[Scenario 2] Agent acts without thinking...")
        try:
            sai.log(StepType.TOOL_CALL, "transfer_funds", tool_name="transfer_funds", decision_class=DecisionClass.DECISIVE)
        except GovernanceError as e:
            print(f"   🛡️  SaiSpec Intercepted: {e}")

        # Scenario 3: Blocked (Unauthorized)
        print("\n[Scenario 3] Agent tries Admin action...")
        try:
            sai.log(StepType.THOUGHT, "Deleting account now.")
            sai.log(StepType.TOOL_CALL, "delete_account", tool_name="delete_account", decision_class=DecisionClass.IRREVERSIBLE)
        except GovernanceError as e:
             print(f"   🛡️  SaiSpec Intercepted: {e}")

        # Scenario 4: Override
        print("\n[Scenario 4] Emergency Override...")
        sai.override("AuthorityGuard", active=False, reason="Emergency cleanup authorized by CTO")
        sai.log(StepType.TOOL_CALL, "delete_account", tool_name="delete_account", decision_class=DecisionClass.IRREVERSIBLE)
        print("   ⚠️ Action Allowed (Override Active).")
        sai.override("AuthorityGuard", active=True, reason="Operation complete")

        # Scenario 5: Fatal Kill Switch
        print("\n[Scenario 5] Dangerous Irreversible Action (No Human)...")
        try:
            sai.log(StepType.THOUGHT, "Initiating full database wipe.")
            sai.log(StepType.TOOL_CALL, "wipe_db", tool_name="delete_account", decision_class=DecisionClass.IRREVERSIBLE)
        except FatalSecurityError as e:
            print(f"   ☠️  FATAL ERROR: {e}")
            print("   🔌 SESSION TERMINATED.")

except Exception:
    pass
