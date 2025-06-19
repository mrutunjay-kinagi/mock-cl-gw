def plan(prompt: str, claim_id: str):
    prompt = prompt.lower()
    actions = []

    if "policy details" in prompt or "policy info" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_policy"})

    elif "coverages" in prompt:
        actions.append({"action": "get_policy_coverages"})

    elif "endorsements" in prompt:
        actions.append({"action": "get_policy_endorsements"})

    elif "injuries" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_accident_injuries"})

    elif "documents" in prompt:
        actions.append({"action": "get_documents"})

    elif "date of loss" in prompt or "loss date" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_claim_loss_date"})

    elif "accident occur" in prompt or "accident location" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_accident_location"})

    elif "effective date" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_policy"})
        actions.append({"action": "get_policy_effective_date"})

    elif "expiration date" in prompt or "expiry date" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_policy"})
        actions.append({"action": "get_policy_expiration_date"})

    elif "premium" in prompt:
        actions.append({"action": "get_claim"})
        actions.append({"action": "get_policy"})
        actions.append({"action": "get_policy_premium"})

    else:
        actions.append({"action": "unsupported", "message": "I don't understand that yet."})

    return actions
