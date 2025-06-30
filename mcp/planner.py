def plan(prompt: str, claim_id: str):
    prompt = prompt.lower()
    actions = set()
    
    if "claim" in prompt or "claim details" in prompt or "claim info" in prompt or "claim detail" in prompt:
        actions.add("get_claim")

    if "policy details" in prompt or "policy info" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")

    if "coverages" in prompt or "coverage" in prompt or "policy coverages" in prompt or "coverage details" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_policy_coverages")

    if "endorsements" in prompt or "policy endorsements" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_policy_endorsements")

    if "injuries" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_accident_injuries")

    if "documents" in prompt:
        actions.add("get_documents")

    if "date of loss" in prompt or "loss date" in prompt:
        actions.add("get_claim")
        actions.add("get_claim_loss_date")

    if "accident occur" in prompt or "accident location" in prompt:
        actions.add("get_claim")
        actions.add("get_accident_location")

    if "effective date" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_policy_effective_date")

    if "expiration date" in prompt or "expiry date" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_policy_expiration_date")

    if "policy period" in prompt or "policy effective date" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_policy_period")

    if "premium" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_policy_premium")

    if "vehicle" in prompt or "vehicle details" in prompt or "vehicle info" in prompt:
        actions.add("get_claim")
        actions.add("get_policy")
        actions.add("get_vehicle_details")

    if not actions:
        actions.add("unsupported")

    return [{"action": action} if action != "unsupported" else {"action": "unsupported", "message": "I don't understand that yet."} for action in actions]