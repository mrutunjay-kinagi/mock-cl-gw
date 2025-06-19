def plan(prompt: str, claim_id: str):
    prompt = prompt.lower()
    actions = []

    if "claim details" in prompt or "claim info" in prompt:
        actions.append({"action": "get_claim"})

    elif "policy details" in prompt or "policy info" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_policy"})

    elif "coverages" in prompt:
        actions.append({"action": "get_policy_coverages"})

    elif "endorsements" in prompt:
        actions.append({"action": "get_policy_endorsements"})

    elif "injuries" in prompt:
        actions.append({"action": "get_injuries"})

    elif "documents" in prompt:
        actions.append({"action": "get_documents"})

    else:
        actions.append({"action": "unsupported", "message": "I don't understand that yet."})

    return actions
