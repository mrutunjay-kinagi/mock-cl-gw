from flask import Flask, jsonify
import json
import os

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(file_name):
    with open(os.path.join(DATA_DIR, file_name)) as f:
        return json.load(f)

# Load all data once at startup
claims = load_json("claims.json")
policies = load_json("policies.json")
documents = load_json("documents.json")
injuries = load_json("injuries.json")
endorsements = load_json("endorsements.json")
coverages = load_json("coverages.json")

@app.route("/claims/<claim_id>")
def get_claim(claim_id):
    return jsonify(claims.get(claim_id, {"error": "Claim not found"}))

@app.route("/claims/<claim_id>/documents")
def get_documents(claim_id):
    return jsonify(documents.get(claim_id, []))

@app.route("/claims/<claim_id>/injuries")
def get_injuries(claim_id):
    return jsonify(injuries.get(claim_id, []))

@app.route("/policies/<policy_id>")
def get_policy(policy_id):
    return jsonify(policies.get(policy_id, {"error": "Policy not found"}))

@app.route("/policies/<policy_id>/coverages")
def get_coverages(policy_id):
    return jsonify(coverages.get(policy_id, []))

@app.route("/policies/<policy_id>/endorsements")
def get_endorsements(policy_id):
    return jsonify(endorsements.get(policy_id, []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)
