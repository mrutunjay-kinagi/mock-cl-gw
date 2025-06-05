from flask import Blueprint, jsonify, request
from utils.sample_data import *
from events.event_handler import EventHandler
from datetime import datetime

claimcenter_bp = Blueprint('claimcenter', __name__)

# Initialize data
claims_data = generate_sample_claims()
policies_data = generate_sample_policies()
documents_data = generate_sample_documents()
incidents_data = generate_sample_injury_incidents()
event_handler = EventHandler()

# Store for activities, notes, etc.
activities_data = {}
notes_data = {}
diagnoses_data = {}
injury_points_data = {}
coverages_data = {
    "cov_1": Coverage("cov_1", "policy_1", "Bodily Injury", 100000.0, 1000.0),
    "cov_2": Coverage("cov_2", "policy_1", "Property Damage", 50000.0, 500.0)
}
endorsements_data = {
    "end_1": Endorsement("end_1", "policy_1", "Additional Coverage", datetime.now(), "Extended coverage endorsement")
}

# ==== CLAIM APIS ====
@claimcenter_bp.route('/claim/v1/claims/<claim_id>', methods=['GET'])
def get_claim(claim_id):
    claim = claims_data.get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    
    return jsonify({
        "claim_id": claim.claim_id,
        "claim_number": claim.claim_number,
        "policy_id": claim.policy_id,
        "status": claim.status,
        "send_to_claim_lens": claim.send_to_claim_lens,
        "created_date": claim.created_date.isoformat(),
        "loss_date": claim.loss_date.isoformat() if claim.loss_date else None,
        "description": claim.description
    })

# ==== INJURY INCIDENT APIS ====
@claimcenter_bp.route('/claim/<claim_id>/injury-incidents', methods=['GET'])
def get_injury_incidents(claim_id):
    incidents = [inc for inc in incidents_data.values() if inc.claim_id == claim_id]
    return jsonify([{
        "incident_id": inc.incident_id,
        "claim_id": inc.claim_id,
        "description": inc.description,
        "severity": inc.severity,
        "body_parts": inc.body_parts
    } for inc in incidents])

@claimcenter_bp.route('/claim/<claim_id>/injury-incidents/<incident_id>', methods=['GET'])
def get_injury_incident(claim_id, incident_id):
    incident = incidents_data.get(incident_id)
    if not incident or incident.claim_id != claim_id:
        return jsonify({"error": "Incident not found"}), 404
    
    return jsonify({
        "incident_id": incident.incident_id,
        "claim_id": incident.claim_id,
        "description": incident.description,
        "severity": incident.severity,
        "body_parts": incident.body_parts
    })

# ==== MEDICAL DIAGNOSES APIS ====
@claimcenter_bp.route('/claim/v1/claims/<claim_id>/injury-incidents/<incident_id>/medical-diagnoses', methods=['GET'])
def get_medical_diagnoses(claim_id, incident_id):
    diagnoses = [diag for diag in diagnoses_data.values() if diag.incident_id == incident_id]
    return jsonify([{
        "diagnosis_id": diag.diagnosis_id,
        "incident_id": diag.incident_id,
        "icd10_code": diag.icd10_code,
        "description": diag.description,
        "diagnosis_date": diag.diagnosis_date.isoformat() if diag.diagnosis_date else None
    } for diag in diagnoses])

# ==== BODILY INJURY POINTS APIS ====
@claimcenter_bp.route('/claim/v1/claims/<claim_id>/injury-incidents/<incident_id>/bodily-injury-points', methods=['GET'])
def get_bodily_injury_points(claim_id, incident_id):
    points = [point for point in injury_points_data.values() if point.incident_id == incident_id]
    return jsonify([{
        "injury_point_id": point.injury_point_id,
        "incident_id": point.incident_id,
        "body_part": point.body_part,
        "injury_type": point.injury_type,
        "severity_level": point.severity_level
    } for point in points])

# ==== POLICY APIS ====
@claimcenter_bp.route('/claim/<claim_id>/policy', methods=['GET'])
def get_policy(claim_id):
    claim = claims_data.get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
        
    policy = policies_data.get(claim.policy_id)
    if not policy:
        return jsonify({"error": "Policy not found"}), 404
    
    return jsonify({
        "policy_id": policy.policy_id,
        "policy_number": policy.policy_number,
        "policy_type": policy.policy_type,
        "effective_date": policy.effective_date.isoformat(),
        "expiration_date": policy.expiration_date.isoformat(),
        "policyholder_name": policy.policyholder_name
    })

# ==== COVERAGE APIS ====
@claimcenter_bp.route('/claims/<claim_id>/policy/coverages', methods=['GET'])
def get_coverages(claim_id):
    claim = claims_data.get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    
    claim_coverages = [cov for cov in coverages_data.values() if cov.policy_id == claim.policy_id]
    return jsonify([{
        "coverage_id": cov.coverage_id,
        "policy_id": cov.policy_id,
        "coverage_type": cov.coverage_type,
        "limit_amount": cov.limit_amount,
        "deductible": cov.deductible,
        "description": cov.description
    } for cov in claim_coverages])

# ==== ENDORSEMENT APIS ====
@claimcenter_bp.route('/claims/<claim_id>/policy/endorsements', methods=['GET'])
def get_endorsements(claim_id):
    claim = claims_data.get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    
    claim_endorsements = [end for end in endorsements_data.values() if end.policy_id == claim.policy_id]
    return jsonify([{
        "endorsement_id": end.endorsement_id,
        "policy_id": end.policy_id,
        "endorsement_type": end.endorsement_type,
        "effective_date": end.effective_date.isoformat(),
        "description": end.description,
        "form_number": end.form_number
    } for end in claim_endorsements])

# ==== DOCUMENT APIS ====
@claimcenter_bp.route('/claim/v1/claims/<claim_id>/documents', methods=['GET'])
def get_documents(claim_id):
    claim_docs = [doc for doc in documents_data.values() if doc.claim_id == claim_id]
    return jsonify([{
        "document_id": doc.document_id,
        "claim_id": doc.claim_id,
        "filename": doc.filename,
        "content_type": doc.content_type,
        "size": doc.size,
        "created_date": doc.created_date.isoformat()
    } for doc in claim_docs])

@claimcenter_bp.route('/claim/v1/claims/<claim_id>/documents/<document_id>/content', methods=['GET'])
def get_document_content(claim_id, document_id):
    doc = documents_data.get(document_id)
    if not doc or doc.claim_id != claim_id:
        return jsonify({"error": "Document not found"}), 404
    
    return jsonify({
        "document_id": doc.document_id,
        "content_base64": doc.content_base64
    })

# ==== NOTES APIS ====
@claimcenter_bp.route('/claim/v1/claims/<claim_id>/notes', methods=['GET'])
def get_notes(claim_id):
    claim_notes = [note for note in notes_data.values() if note.claim_id == claim_id]
    return jsonify([{
        "note_id": note.note_id,
        "claim_id": note.claim_id,
        "content": note.content,
        "note_type": note.note_type,
        "created_by": note.created_by,
        "created_date": note.created_date.isoformat()
    } for note in claim_notes])

# ==== ACTIVITIES APIS ====
@claimcenter_bp.route('/claim/v1/claims/<claim_id>/activities', methods=['GET'])
def get_activities(claim_id):
    claim_activities = [act for act in activities_data.values() if act.claim_id == claim_id]
    return jsonify([{
        "activity_id": act.activity_id,
        "claim_id": act.claim_id,
        "activity_type": act.activity_type,
        "description": act.description,
        "assigned_user": act.assigned_user,
        "status": act.status,
        "created_date": act.created_date.isoformat()
    } for act in claim_activities])

# ==== EVENT SIMULATION ENDPOINT ====
@claimcenter_bp.route('/claim/v1/claims/<claim_id>/trigger-event', methods=['POST'])
def trigger_claim_event(claim_id):
    """Simulate triggering a Claim:Create or Claim:Update event"""
    claim = claims_data.get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404
    
    event_type = request.json.get('event_type', 'Claim:Update')
    
    # Create event
    event = event_handler.create_claim_event(
        event_type=event_type,
        claim_id=claim_id,
        claim_data={
            "claim_id": claim.claim_id,
            "claim_number": claim.claim_number,
            "send_to_claim_lens": claim.send_to_claim_lens,
            "status": claim.status
        }
    )
    
    # Simulate messaging
    if claim.send_to_claim_lens:
        result = event_handler.simulate_messaging_to_claimlens(event)
        return jsonify({
            "message": "Event triggered and sent to ClaimLens",
            "event": {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "claim_id": event.claim_id,
                "timestamp": event.timestamp.isoformat()
            },
            "messaging_result": result
        })
    else:
        return jsonify({
            "message": "Event triggered but not sent to ClaimLens (sendToClaimLens=False)",
            "event": {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "claim_id": event.claim_id,
                "timestamp": event.timestamp.isoformat()
            }
        })