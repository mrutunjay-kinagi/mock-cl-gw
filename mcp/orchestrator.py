from flask import Flask, request, jsonify
import requests
from planner import plan
import json

app = Flask(__name__)

CLAIMCENTER_BASE = "http://claimcenter-api:8080"
CLAIMLENS_BASE = "http://claimlens-api:5001"


@app.route("/orchestrate", methods=["POST"])
def orchestrate():
    print("=== ORCHESTRATOR REQUEST ===")
    data = request.json
    print(f"Incoming request data: {json.dumps(data, indent=2)}")

    prompt = data.get("prompt", "")
    claim_id = data.get("claim_id", "")
    print(f"Extracted - Prompt: '{prompt}', Claim ID: '{claim_id}'")

    if not prompt or not claim_id:
        error_response = {"error": "Missing prompt or claim_id"}
        print(f"ERROR: {error_response}")
        return jsonify(error_response), 400

    steps = plan(prompt, claim_id)
    print(f"Planned steps: {json.dumps(steps, indent=2)}")


    outputs = []
    claim = {}
    policy = {}

    url = f"{CLAIMCENTER_BASE}/claims/{claim_id}"
    print(f"Making request to: {url}")
    claim_resp = requests.get(url)
    print(f"Response status: {claim_resp.status_code}")
    claim = claim_resp.json()
    policy_id = claim.get("policy_id", "")
    
    
    try:
        for i, step in enumerate(steps):
            action = step["action"]
            print(f"\n--- Executing Step {i+1}: {action} ---")

            if action == "get_claim":
                url = f"{CLAIMCENTER_BASE}/claims/{claim_id}"
                print(f"Making request to: {url}")
                claim_resp = requests.get(url)
                print(f"Response status: {claim_resp.status_code}")
                claim = claim_resp.json()
                policy_id = claim.get("policy_id", "")
                print(f"Claim data received: {json.dumps(claim, indent=2)}")
                outputs.append({"step": "Claim retrieved", "data": claim})

            elif action == "get_policy":
                policy_id = claim.get("policy_id")
                print(f"Policy ID from claim: {policy_id}")
                if policy_id:
                    url = f"{CLAIMCENTER_BASE}/policies/{policy_id}"
                    print(f"Making request to: {url}")
                    policy_resp = requests.get(url)
                    print(f"Response status: {policy_resp.status_code}")
                    policy = policy_resp.json()
                    print(f"Policy data received: {json.dumps(policy, indent=2)}")
                    outputs.append({"step": "Policy details fetched", "data": policy})

            elif action == "get_policy_coverages":
                if policy_id:
                    url = f"{CLAIMCENTER_BASE}/policies/{policy_id}/coverages"
                    print(f"Making request to: {url}")
                    cov_resp = requests.get(url)
                    print(f"Response status: {cov_resp.status_code}")
                    coverage_data = cov_resp.json()
                    print(
                        f"Coverage data received: {json.dumps(coverage_data, indent=2)}"
                    )
                    outputs.append(
                        {"step": "Policy coverages fetched", "data": coverage_data}
                    )
                else:
                    print("ERROR: No policy_id found for coverage lookup")
                    outputs.append(
                        {
                            "step": "Coverage lookup failed",
                            "message": "No policy_id found.",
                        }
                    )

            elif action == "get_policy_endorsements":
                if policy_id:
                    url = f"{CLAIMCENTER_BASE}/policies/{policy_id}/endorsements"
                    print(f"Making request to: {url}")
                    end_resp = requests.get(url)
                    print(f"Response status: {end_resp.status_code}")
                    endorsement_data = end_resp.json()
                    print(
                        f"Endorsement data received: {json.dumps(endorsement_data, indent=2)}"
                    )
                    outputs.append(
                        {
                            "step": "Policy endorsements fetched",
                            "data": endorsement_data,
                        }
                    )
                else:
                    print("ERROR: No policy_id found for endorsement lookup")
                    outputs.append(
                        {
                            "step": "Endorsement lookup failed",
                            "message": "No policy_id found.",
                        }
                    )

            elif action == "get_documents":
                url = f"{CLAIMCENTER_BASE}/claims/{claim_id}/documents"
                print(f"Making request to: {url}")
                doc_resp = requests.get(url)
                print(f"Response status: {doc_resp.status_code}")
                doc_data = doc_resp.json()
                print(f"Document data received: {json.dumps(doc_data, indent=2)}")
                outputs.append({"step": "Documents retrieved", "data": doc_data})

            elif action == "get_injuries":
                url = f"{CLAIMCENTER_BASE}/claims/{claim_id}/injuries"
                print(f"Making request to: {url}")
                injury_resp = requests.get(url)
                print(f"Response status: {injury_resp.status_code}")
                injury_data = injury_resp.json()
                print(f"Injury data received: {json.dumps(injury_data, indent=2)}")
                outputs.append({"step": "Injuries retrieved", "data": injury_data})

            elif action == "get_claim_loss_date":
                loss_date = claim.get("loss_date", "Not found")
                print(f"Loss date extracted: {loss_date}")
                outputs.append({"step": "Loss Date", "data": loss_date})

            elif action == "get_accident_location":
                location = claim.get("accident_details", {}).get("location", {})
                print(f"Accident location extracted: {json.dumps(location, indent=2)}")
                outputs.append({"step": "Accident Location", "data": location})

            elif action == "get_accident_injuries":
                injuries = claim.get("accident_details", {}).get("injuries", [])
                print(f"Accident injuries extracted: {json.dumps(injuries, indent=2)}")
                outputs.append({"step": "Injury Details", "data": injuries})

            # elif action == "get_policy_effective_date":
            #     effective_date = policy.get("effective_date", "Not found")
            #     print(f"Policy effective date extracted: {effective_date}")
            #     outputs.append({
            #         "step": "Policy Effective Date",
            #         "data": effective_date
            #     })

            # elif action == "get_policy_expiration_date":
            #     expiration_date = policy.get("expiration_date", "Not found")
            #     print(f"Policy expiration date extracted: {expiration_date}")
            #     outputs.append({
            #         "step": "Policy Expiration Date",
            #         "data": expiration_date
            #     })

            elif action == "get_policy_period":
                period_data = f"From {policy.get('effective_date', 'N/A')} to {policy.get('expiration_date', 'N/A')}"
                print(f"Policy period extracted: {json.dumps(period_data, indent=2)}")
                outputs.append({"step": "Policy Period", "data": period_data})

            elif action == "get_policy_premium":
                premium = f"${policy.get('premium', 0):,.2f}"
                print(f"Policy premium extracted: {premium}")
                outputs.append({"step": "Policy Premium", "data": premium})

            elif action == "get_vehicle_details":
                url = f"{CLAIMCENTER_BASE}/policies/{policy_id}"
                print(f"Making request to: {url}")
                vehicle_resp = requests.get(url)
                if vehicle_resp.status_code != 200:
                    raise Exception(
                        f"Failed to fetch vehicle details, status code: {vehicle_resp.status_code}"
                    )
                print(f"Vehicle details response status: {vehicle_resp.status_code}")
                vehicle_data = vehicle_resp.json().get("vehicle_details", {})
                if not vehicle_data:
                    raise Exception("No vehicle details found in policy response")
                print(f"Vehicle data received: {json.dumps(vehicle_data, indent=2)}")
                outputs.append(
                    {"step": "Vehicle details fetched", "data": vehicle_data}
                )

            elif action == "unsupported":
                print(f"Unsupported action with message: {step['message']}")
                outputs.append(
                    {
                        "step": "Unsupported prompt",
                        "message": step["message"],
                        "data": "N/A",
                    }
                )

        final_response = {
            "prompt": prompt,
            "claim_id": claim_id,
            "steps_executed": [s["step"] for s in outputs],
            "results": outputs,
        }

        print("\n=== FINAL ORCHESTRATOR RESPONSE ===")
        print(json.dumps(final_response, indent=2))
        print("====================================")

        return jsonify(final_response)

    except Exception as e:
        error_response = {"error": str(e)}
        print(f"\n=== ORCHESTRATOR ERROR ===")
        print(f"Exception: {str(e)}")
        print(f"Error response: {json.dumps(error_response, indent=2)}")
        print("=========================")
        return jsonify(error_response), 500


if __name__ == "__main__":
    print("Starting MCP Orchestrator on port 8002...")
    app.run(host="0.0.0.0", port=8002,debug=True)
