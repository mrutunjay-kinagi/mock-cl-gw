from flask import Blueprint, jsonify, request
from models.claim_models import *
import uuid
from datetime import datetime

claimlens_bp = Blueprint('claimlens', __name__)

# Import data stores from claimcenter routes
from routes.claimcenter_routes import activities_data, notes_data, documents_data, diagnoses_data, injury_points_data

# ==== CLAIMLENS WEBHOOK (Receives events from ClaimCenter) ====
@claimlens_bp.route('/claimlens/webhook/claim-event', methods=['POST'])
def receive_claim_event():
    """Simulate ClaimLens receiving Claim:Create or Claim:Update events"""
    event_data = request.json
    
    print(f"🔍 ClaimLens received event: {event_data.get('event_type')} for claim {event_data.get('claim_id')}")
    
    # Simulate AI processing
    claim_id = event_data.get('claim_id')
    processing_result = {
        "event_id": event_data.get('event_id'),
        "claim_id": claim_id,
        "processing_status": "completed",
        "ai_analysis": {
            "risk_score": 7.5,
            "complexity_level": "High",
            "recommended_actions": [
                "Review medical documentation",
                "Verify coverage limits",
                "Schedule adjuster review"
            ],
            "potential_issues": [
                "Coverage mismatch detected",
                "High medical costs indicated"
            ]
        },
        "processed_at": datetime.now().isoformat()
    }
    
    return jsonify(processing_result)

# ==== APIS FOR WRITING BACK TO CLAIMCENTER ====
@claimlens_bp.route('/claim/v1/claims/<claim_id>/activities', methods=['POST'])
def create_activity(claim_id):
    """ClaimLens creates activities in ClaimCenter"""
    data = request.json
    
    activity = Activity(
        activity_id=str(uuid.uuid4()),
        claim_id=claim_id,
        activity_type=data.get('activity_type', 'AI_Analysis'),
        description=data.get('description', 'AI-generated activity'),
        assigned_user=data.get('assigned_user'),
        status=data.get('status', 'Open')
    )
    
    activities_data[activity.activity_id] = activity
    
    return jsonify({
        "activity_id": activity.activity_id,
        "claim_id": activity.claim_id,
        "activity_type": activity.activity_type,
        "description": activity.description,
        "status": "created"
    }), 201

@claimlens_bp.route('/claim/v1/claims/<claim_id>/notes', methods=['POST'])
def create_note(claim_id):
    """ClaimLens creates notes in ClaimCenter"""
    data = request.json
    
    note = Note(
        note_id=str(uuid.uuid4()),
        claim_id=claim_id,
        content=data.get('content', 'AI-generated note'),
        note_type=data.get('note_type', 'AI_Analysis'),
        created_by=data.get('created_by', 'ClaimLens_AI')
    )
    
    notes_data[note.note_id] = note
    
    return jsonify({
        "note_id": note.note_id,
        "claim_id": note.claim_id,
        "content": note.content,
        "note_type": note.note_type,
        "status": "created"
    }), 201

@claimlens_bp.route('/claim/v1/claims/<claim_id>/documents', methods=['POST'])
def create_document(claim_id):
    """ClaimLens uploads documents to ClaimCenter"""
    data = request.json
    
    document = Document(
        document_id=str(uuid.uuid4()),
        claim_id=claim_id,
        filename=data.get('filename', 'ai_summary.pdf'),
        content_type=data.get('content_type', 'application/pdf'),
        size=data.get('size', 1024),
        content_base64=data.get('content_base64')
    )
    
    documents_data[document.document_id] = document
    
    return jsonify({
        "document_id": document.document_id,
        "claim_id": document.claim_id,
        "filename": document.filename,
        "status": "created"
    }), 201

@claimlens_bp.route('/claim/v1/claims/<claim_id>/injury-incidents/<incident_id>/medical-diagnoses', methods=['POST'])
def create_medical_diagnosis(claim_id, incident_id):
    """ClaimLens creates medical diagnoses"""
    data = request.json
    
    diagnosis = MedicalDiagnosis(
        diagnosis_id=str(uuid.uuid4()),
        incident_id=incident_id,
        icd10_code=data.get('icd10_code', 'M54.5'),
        description=data.get('description', 'AI-identified diagnosis'),
        diagnosis_date=datetime.now()
    )
    
    diagnoses_data[diagnosis.diagnosis_id] = diagnosis
    
    return jsonify({
        "diagnosis_id": diagnosis.diagnosis_id,
        "incident_id": diagnosis.incident_id,
        "icd10_code": diagnosis.icd10_code,
        "description": diagnosis.description,
        "status": "created"
    }), 201

@claimlens_bp.route('/claim/v1/claims/<claim_id>/injury-incidents/<incident_id>/medical-diagnoses/<diagnosis_id>', methods=['PATCH'])
def update_medical_diagnosis(claim_id, incident_id, diagnosis_id):
    """ClaimLens updates medical diagnoses"""
    diagnosis = diagnoses_data.get(diagnosis_id)
    if not diagnosis:
        return jsonify({"error": "Diagnosis not found"}), 404
    
    data = request.json
    if 'icd10_code' in data:
        diagnosis.icd10_code = data['icd10_code']
    if 'description' in data:
        diagnosis.description = data['description']
    
    return jsonify({
        "diagnosis_id": diagnosis.diagnosis_id,
        "incident_id": diagnosis.incident_id,
        "icd10_code": diagnosis.icd10_code,
        "description": diagnosis.description,
        "status": "updated"
    })

@claimlens_bp.route('/claim/v1/claims/<claim_id>/injury-incidents/<incident_id>/bodily-injury-points/<injury_point_id>', methods=['PATCH'])
def update_bodily_injury_point(claim_id, incident_id, injury_point_id):
    """ClaimLens updates bodily injury points"""
    injury_point = injury_points_data.get(injury_point_id)
    if not injury_point:
        return jsonify({"error": "Injury point not found"}), 404
    
    data = request.json
    if 'body_part' in data:
        injury_point.body_part = data['body_part']
    if 'injury_type' in data:
        injury_point.injury_type = data['injury_type']
    if 'severity_level' in data:
        injury_point.severity_level = data['severity_level']
    
    return jsonify({
        "injury_point_id": injury_point.injury_point_id,
        "incident_id": injury_point.incident_id,
        "body_part": injury_point.body_part,
        "injury_type": injury_point.injury_type,
        "severity_level": injury_point.severity_level,
        "status": "updated"
    })

# ==== CLAIMLENS CHAT SERVICE ====
@claimlens_bp.route('/claimlens/chat/session', methods=['GET'])
def get_chat_session():
    """Mock ClaimLens chat session endpoint"""
    claim_id = request.args.get('claim_id')
    return jsonify({
        "session_id": str(uuid.uuid4()),
        "claim_id": claim_id,
        "chat_url": f"https://claimlens.example.doclens.ai/chat/{claim_id}",
        "status": "active"
    })

@claimlens_bp.route('/claimlens/chat/message', methods=['POST'])
def chat_message():
    """Mock conversational chat endpoint"""
    data = request.json
    user_message = data.get('message', '')
    claim_id = data.get('claim_id')
    
    # Simple mock response
    ai_response = f"Based on my analysis of claim {claim_id}, I can help you with: {user_message}. Here are the key findings..."
    
    return jsonify({
        "response": ai_response,
        "claim_id": claim_id,
        "confidence": 0.85,
        "sources": ["Medical Report 1", "Policy Document", "Loss Notice"]
    })