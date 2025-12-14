import time
from saispec import (
    SaiRecorder, AgentContext, DecisionClass, Severity, StepType,
    AuthorityGuard, AccountabilityGuard, ImpactAwareness, NoLoops,
    GovernanceError, FatalSecurityError
)

# ==========================================
# 1. SETUP: Define the Rules of Engagement
# ==========================================

# A. Define Permissions (Role-Based Access Control)
tool_permissions = {
    "transfer_funds": ["finance_access"], 
    "delete_account": ["admin_root"],
    "refund_user": ["support_lead"]
}

# B. Define the User Context (The "Driver's License")
# This user is a 'Support Lead' but NOT an Admin.
context = AgentContext(
    user_id="user_123",
    permissions=["support_lead", "finance_access"], 
    has_user_consent=True,
    human_in_loop=False  # No human is watching (Critical for ImpactAwareness)
)

# C. Load the Guards
specs = [
    AuthorityGuard(tool_permissions),
    AccountabilityGuard(min_thought_length=10),
    ImpactAwareness(),
    NoLoops(max_retries=2)
]

print("\n🛡️  SAISPEC GOVERNANCE SYSTEM | INITIALIZING...")
print(f"👤 User Context: {context.user_id} | Perms: {context.permissions}")
print("----------------------------------------------------------------")

# ==========================================
# 2. RUN THE SIMULATION
# ==========================================

try:
    with SaiRecorder(specs=specs, context=context) as sai:
        
        # --- SCENARIO 1: The Good Action (Success) ---
        print("\n[Scenario 1] Valid Refund Request...")
        sai.log(StepType.THOUGHT, "User requested a refund. I have verified the transaction.")
        sai.log(StepType.TOOL_CALL, "refund_user", tool_name="refund_user", decision_class=DecisionClass.DECISIVE)
        print("   ✅ Action Allowed.")

        # --- SCENARIO 2: The Unaccountable Action (Blocked) ---
        print("\n[Scenario 2] Agent acts without thinking...")
        try:
            # Agent calls a risky tool WITHOUT a preceding thought
            sai.log(StepType.TOOL_CALL, "transfer_funds", tool_name="transfer_funds", decision_class=DecisionClass.DECISIVE)
        except GovernanceError as e:
            print(f"   🛡️  SaiSpec Intercepted: {e}")

        # --- SCENARIO 3: The Unauthorized Action (Blocked) ---
        print("\n[Scenario 3] Agent tries Admin action...")
        try:
            sai.log(StepType.THOUGHT, "I will now delete the user account to clean up.")
            # Agent tries 'delete_account' but lacks 'admin_root' permission
            sai.log(StepType.TOOL_CALL, "delete_account", tool_name="delete_account", decision_class=DecisionClass.IRREVERSIBLE)
        except GovernanceError as e:
             print(f"   🛡️  SaiSpec Intercepted: {e}")

        # --- SCENARIO 4: The Audit Override (Governance) ---
        print("\n[Scenario 4] Emergency Override...")
        # We temporarily disable the AuthorityGuard
        sai.override("AuthorityGuard", active=False, reason="Emergency cleanup authorized by CTO")
        
        # Now the previously blocked action succeeds (but is audited)
        sai.log(StepType.TOOL_CALL, "delete_account", tool_name="delete_account", decision_class=DecisionClass.IRREVERSIBLE)
        print("   ⚠️ Action Allowed (Override Active).")
        
        # Re-enable for safety
        sai.override("AuthorityGuard", active=True, reason="Operation complete")

        # --- SCENARIO 5: The Kill Switch (Fatal) ---
        print("\n[Scenario 5] Dangerous Irreversible Action (No Human)...")
        try:
            sai.log(StepType.THOUGHT, "Initiating full database wipe.")
            # ImpactAwareness checks: Is Irreversible? Yes. Is Human watching? No. -> KILL.
            sai.log(StepType.TOOL_CALL, "wipe_db", tool_name="delete_account", decision_class=DecisionClass.IRREVERSIBLE)
        except FatalSecurityError as e:
            print(f"   ☠️  FATAL ERROR: {e}")
            print("   🔌 SESSION TERMINATED.")

except Exception as e:
    pass # Catch the fatal error to show the report

# ==========================================
# 3. THE REPORT
# ==========================================
# (Report prints automatically on exit)