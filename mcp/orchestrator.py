from flask import Flask, request, jsonify
import requests
from planner import plan

app = Flask(__name__)

CLAIMCENTER_BASE = "http://claimcenter-api:8080"
CLAIMLENS_BASE = "http://claimlens-api:5001"

@app.route("/orchestrate", methods=["POST"])
def orchestrate():
    data = request.json
    prompt = data.get("prompt", "")
    claim_id = data.get("claim_id", "")

    if not prompt or not claim_id:
        return jsonify({"error": "Missing prompt or claim_id"}), 400

    steps = plan(prompt, claim_id)
    outputs = []
    claim = {}
    policy = {}
    try :
        for step in steps:
            action = step["action"]
            
            if action == "get_claim":
                claim_resp = requests.get(f"{CLAIMCENTER_BASE}/claims/{claim_id}")
                claim = claim_resp.json()
                outputs.append({"step": "Claim retrieved", "data": claim})

            elif action == "get_policy":
                policy_id = claim.get("policy_id")
                if policy_id:
                    policy_resp = requests.get(f"{CLAIMCENTER_BASE}/policies/{policy_id}")
                    policy = policy_resp.json()
                    outputs.append({"step": "Policy details fetched", "data": policy})

            elif action == "get_policy_coverages":
                if policy.get("policy_id"):
                    cov_resp = requests.get(f"{CLAIMCENTER_BASE}/policies/{policy['policy_id']}/coverages")
                    outputs.append({"step": "Policy coverages fetched", "data": cov_resp.json()})
                else:
                    outputs.append({"step": "Coverage lookup failed", "message": "No policy_id found."})

            elif action == "get_policy_endorsements":
                if policy.get("policy_id"):
                    end_resp = requests.get(f"{CLAIMCENTER_BASE}/policies/{policy['policy_id']}/endorsements")
                    outputs.append({"step": "Policy endorsements fetched", "data": end_resp.json()})
                else:
                    outputs.append({"step": "Endorsement lookup failed", "message": "No policy_id found."})

            elif action == "get_documents":
                doc_resp = requests.get(f"{CLAIMCENTER_BASE}/claims/{claim_id}/documents")
                outputs.append({"step": "Documents retrieved", "data": doc_resp.json()})

            elif action == "get_injuries":
                injury_resp = requests.get(f"{CLAIMCENTER_BASE}/claims/{claim_id}/injuries")
                outputs.append({"step": "Injuries retrieved", "data": injury_resp.json()})
            
            elif action == "get_claim_loss_date":
                outputs.append({
                    "step": "Loss Date",
                    "data": claim.get("loss_date", "Not found")
                })

            elif action == "get_accident_location":
                outputs.append({
                    "step": "Accident Location",
                    "data": claim.get("accident_details", {}).get("location", {})
                })

            elif action == "get_accident_injuries":
                outputs.append({
                    "step": "Injury Details",
                    "data": claim.get("accident_details", {}).get("injuries", [])
                })

            elif action == "get_policy_effective_date":
                outputs.append({
                    "step": "Policy Effective Date",
                    "data": policy.get("effective_date", "Not found")
                })

            elif action == "get_policy_expiration_date":
                outputs.append({
                    "step": "Policy Expiration Date",
                    "data": policy.get("expiration_date", "Not found")
                })

            elif action == "get_policy_premium":
                outputs.append({
                    "step": "Policy Premium",
                    "data": f"${policy.get('premium', 0):,.2f}"
                })

            elif action == "unsupported":
                outputs.append({"step": "Unsupported prompt", "message": step["message"]})
    
        return jsonify({
            "prompt": prompt,
            "claim_id": claim_id,
            "steps_executed": [s["step"] for s in outputs],
            "results": outputs
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
