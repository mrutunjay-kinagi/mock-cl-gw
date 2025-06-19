from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    claim_id = data.get("claim_id")

    return jsonify({
        "claim_id": claim_id,
        "risk_score": 8.5,
        "key_findings": [
            "Medical records indicate pre-existing condition",
            "Treatment plan is reasonable and necessary"
        ],
        "recommended_actions": [
            {"priority": "High", "action": "Request updated medical records"},
            {"priority": "Medium", "action": "Schedule independent medical examination"}
        ],
        "coverage_analysis": {
            "adequacy": "Adequate",
            "gaps": ["Rental car coverage may be insufficient"]
        },
        "icd10_codes": [
            {"code": "M54.5", "description": "Low back pain"},
            {"code": "S13.4", "description": "Sprain of cervical spine"}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
