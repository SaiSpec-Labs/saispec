from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from enum import Enum
import datetime
import uuid

# --- 1. GOVERNANCE ENUMS ---
class DecisionClass(Enum):
    INFORMATIONAL = "INFO"      # Read-only (Google Search)
    ADVISORY = "ADVISORY"       # Recommendations (Draft Email)
    DECISIVE = "DECISIVE"       # Actions (Send Email, Buy Stock)
    IRREVERSIBLE = "CRITICAL"   # Destructive (Delete DB, Transfer Funds)

class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCK = "BLOCK"             # Stop this specific action
    STOP_IMMEDIATE = "FATAL"    # Kill the agent entirely

# --- 2. CONTEXT (The License) ---
@dataclass
class AgentContext:
    """The 'Driver's License' for the current session."""
    user_id: str
    permissions: List[str] = field(default_factory=list)  # e.g. ['can_refund', 'admin']
    has_user_consent: bool = False
    human_in_loop: bool = False

# --- 3. THE TRACE (The Black Box) ---
@dataclass
class TraceStep:
    step_type: str  # 'thought', 'tool_call', 'system_audit'
    content: Any
    tool_name: Optional[str] = None
    
    # Governance Tags
    decision_class: DecisionClass = DecisionClass.INFORMATIONAL
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    # Audit Flags (Did the user override safety here?)
    is_override: bool = False
    override_reason: Optional[str] = None

@dataclass
class Violation:
    spec_name: str
    message: str
    severity: Severity
    decision_class: str
    correction_prompt: Optional[str] = None  # The self-healing instruction
