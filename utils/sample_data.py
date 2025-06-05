from datetime import datetime, timedelta
from models.claim_models import *
from models.policy_models import *
import uuid
import base64

def generate_sample_claims():
    return {
        "claim_1": Claim(
            claim_id="claim_1",
            claim_number="CL-2024-001",
            policy_id="policy_1",
            send_to_claim_lens=True,
            status="Open",
            loss_date=datetime.now() - timedelta(days=30),
            description="Auto accident with injuries"
        ),
        "claim_2": Claim(
            claim_id="claim_2",
            claim_number="CL-2024-002",
            policy_id="policy_2",
            send_to_claim_lens=False,
            status="Open",
            loss_date=datetime.now() - timedelta(days=15),
            description="Property damage claim"
        )
    }

def generate_sample_policies():
    return {
        "policy_1": Policy(
            policy_id="policy_1",
            policy_number="POL-2024-001",
            policy_type="Auto",
            effective_date=datetime.now() - timedelta(days=365),
            expiration_date=datetime.now() + timedelta(days=365),
            policyholder_name="John Doe"
        ),
        "policy_2": Policy(
            policy_id="policy_2",
            policy_number="POL-2024-002",
            policy_type="Homeowners",
            effective_date=datetime.now() - timedelta(days=200),
            expiration_date=datetime.now() + timedelta(days=565),
            policyholder_name="Jane Smith"
        )
    }

def generate_sample_documents():
    sample_pdf_content = "Sample PDF content for medical records"
    return {
        "doc_1": Document(
            document_id="doc_1",
            claim_id="claim_1",
            filename="medical_report.pdf",
            content_type="application/pdf",
            size=1024,
            content_base64=base64.b64encode(sample_pdf_content.encode()).decode()
        )
    }

def generate_sample_injury_incidents():
    return {
        "incident_1": InjuryIncident(
            incident_id="incident_1",
            claim_id="claim_1",
            description="Back injury from auto accident",
            severity="Moderate",
            body_parts=["Lower Back", "Neck"]
        )
    }