from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class Claim:
    claim_id: str
    claim_number: str
    policy_id: str
    send_to_claim_lens: bool = False
    status: str = "Open"
    created_date: datetime = field(default_factory=datetime.now)
    loss_date: Optional[datetime] = None
    description: Optional[str] = None

@dataclass
class InjuryIncident:
    incident_id: str
    claim_id: str
    description: str
    severity: str = "Minor"
    body_parts: List[str] = field(default_factory=list)

@dataclass
class MedicalDiagnosis:
    diagnosis_id: str
    incident_id: str
    icd10_code: str
    description: str
    diagnosis_date: Optional[datetime] = None

@dataclass
class BodilyInjuryPoint:
    injury_point_id: str
    incident_id: str
    body_part: str
    injury_type: str
    severity_level: int = 1

@dataclass
class Activity:
    activity_id: str
    claim_id: str
    activity_type: str
    description: str
    assigned_user: Optional[str] = None
    status: str = "Open"
    created_date: datetime = field(default_factory=datetime.now)

@dataclass
class Note:
    note_id: str
    claim_id: str
    content: str
    note_type: str = "General"
    created_by: str = "System"
    created_date: datetime = field(default_factory=datetime.now)

@dataclass
class Document:
    document_id: str
    claim_id: str
    filename: str
    content_type: str
    size: int
    content_base64: Optional[str] = None
    created_date: datetime = field(default_factory=datetime.now)