from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Policy:
    policy_id: str
    policy_number: str
    policy_type: str
    effective_date: datetime
    expiration_date: datetime
    policyholder_name: str

@dataclass
class Coverage:
    coverage_id: str
    policy_id: str
    coverage_type: str
    limit_amount: float
    deductible: float = 0.0
    description: Optional[str] = None

@dataclass
class Endorsement:
    endorsement_id: str
    policy_id: str
    endorsement_type: str
    effective_date: datetime
    description: str
    form_number: Optional[str] = None