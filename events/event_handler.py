from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
import json
import uuid

@dataclass
class ClaimEvent:
    event_id: str
    event_type: str  # "Claim:Create" or "Claim:Update"
    claim_id: str
    timestamp: datetime
    payload: Dict[str, Any]
    send_to_claim_lens: bool = False

class EventHandler:
    def __init__(self):
        self.events = []
        
    def create_claim_event(self, event_type: str, claim_id: str, claim_data: Dict[str, Any]) -> ClaimEvent:
        event = ClaimEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            claim_id=claim_id,
            timestamp=datetime.now(),
            payload=claim_data,
            send_to_claim_lens=claim_data.get('send_to_claim_lens', False)
        )
        self.events.append(event)
        return event
    
    def get_events_for_claim_lens(self) -> list:
        return [event for event in self.events if event.send_to_claim_lens]
    
    def simulate_messaging_to_claimlens(self, event: ClaimEvent):
        """Simulate sending event to ClaimLens via Guidewire Messaging/EventBridge"""
        print(f"📤 Sending {event.event_type} event for claim {event.claim_id} to ClaimLens")
        return {
            "event_id": event.event_id,
            "status": "sent",
            "destination": "claimlens-api-gateway"
        }