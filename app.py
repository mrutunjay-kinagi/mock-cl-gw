from flask import Flask, jsonify
from routes.claimcenter_routes import claimcenter_bp
from routes.claimlens_routes import claimlens_bp
from events.event_handler import EventHandler

app = Flask(__name__)

# Register blueprints
app.register_blueprint(claimcenter_bp, url_prefix='/claimcenter')
app.register_blueprint(claimlens_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        "message": "ClaimCenter & ClaimLens Mock APIs",
        "endpoints": {
            "claimcenter": {
                "claims": "/claimcenter/claim/v1/claims/{claim_id}",
                "trigger_event": "/claimcenter/claim/v1/claims/{claim_id}/trigger-event",
                "documents": "/claimcenter/claim/v1/claims/{claim_id}/documents",
                "notes": "/claimcenter/claim/v1/claims/{claim_id}/notes",
                "activities": "/claimcenter/claim/v1/claims/{claim_id}/activities"
            },
            "claimlens": {
                "webhook": "/api/claimlens/webhook/claim-event",
                "create_activity": "/api/claim/v1/claims/{claim_id}/activities",
                "create_note": "/api/claim/v1/claims/{claim_id}/notes",
                "chat": "/api/claimlens/chat/session"
            }
        },
        "sample_data": {
            "claims": ["claim_1", "claim_2"],
            "policies": ["policy_1", "policy_2"]
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "claimcenter-claimlens-mock"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)