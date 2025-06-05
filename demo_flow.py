"""
ClaimCenter & ClaimLens Integration Demo Flow

This script demonstrates the complete integration flow:
1. Claim Create/Update Event → ClaimLens
2. ClaimLens Data Retrieval from ClaimCenter
3. AI Analysis Processing
4. Results Written Back to ClaimCenter
"""

import requests
import json
import time
from datetime import datetime
import base64

# Configuration
BASE_URL = "http://localhost:5000"
CLAIMCENTER_URL = f"{BASE_URL}/claimcenter"
CLAIMLENS_URL = f"{BASE_URL}/api"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n🔸 STEP {step_num}: {description}")
    print("-" * 50)

def print_response(response, title="Response"):
    """Pretty print API response"""
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ {title} (Status: {response.status_code})")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ {title} (Status: {response.status_code})")
        print(response.text)

def simulate_delay(seconds=1):
    """Simulate processing delay"""
    print(f"⏳ Processing... ({seconds}s)")
    time.sleep(seconds)

class ClaimLensIntegrationDemo:
    def __init__(self):
        self.claim_id = "claim_1"  # Use existing sample claim
        self.event_data = None
        self.retrieved_data = {}
        self.ai_analysis_results = {}
        
    def run_complete_demo(self):
        """Run the complete integration demo"""
        print_section("ClaimCenter & ClaimLens Integration Demo")
        print("Simulating the complete bidirectional integration flow...")
        
        # Phase 1: Event-Driven Activation
        self.phase_1_event_triggering()
        
        # Phase 2: Data Retrieval
        self.phase_2_data_retrieval()
        
        # Phase 3: AI Analysis
        self.phase_3_ai_analysis()
        
        # Phase 4: Writing Results Back
        self.phase_4_write_results_back()
        
        # Phase 5: Verification
        self.phase_5_verification()
        
        print_section("Demo Complete!")
        print("✅ Successfully demonstrated the complete ClaimLens integration flow!")

    def phase_1_event_triggering(self):
        """Phase 1: Demonstrate event-driven activation"""
        print_section("PHASE 1: Event-Driven Activation")
        
        print_step(1, "Check Initial Claim State")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}")
        print_response(response, "Initial Claim Data")
        
        claim_data = response.json()
        print(f"📋 Claim {claim_data['claim_number']} has sendToClaimLens = {claim_data['send_to_claim_lens']}")
        
        simulate_delay(2)
        
        print_step(2, "Trigger Claim:Update Event")
        print("🎯 Simulating adjuster updating claim in ClaimCenter UI...")
        
        event_payload = {
            "event_type": "Claim:Update",
            "trigger_reason": "Adjuster updated claim with new medical documents"
        }
        
        response = requests.post(
            f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/trigger-event",
            json=event_payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "Event Trigger Result")
        
        self.event_data = response.json()
        simulate_delay(1)

    def phase_2_data_retrieval(self):
        """Phase 2: ClaimLens retrieves comprehensive data from ClaimCenter"""
        print_section("PHASE 2: Comprehensive Data Ingestion")
        print("🔍 ClaimLens received the event and now retrieves all claim data...")
        
        # Simulate ClaimLens receiving the event
        print_step(1, "ClaimLens Receives Event via EventBridge/API Gateway")
        webhook_payload = {
            "event_type": "Claim:Update",
            "claim_id": self.claim_id,
            "event_id": self.event_data.get('event', {}).get('event_id', 'evt_123'),
            "timestamp": datetime.now().isoformat(),
            "source": "ClaimCenter"
        }
        
        response = requests.post(
            f"{CLAIMLENS_URL}/claimlens/webhook/claim-event",
            json=webhook_payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "ClaimLens Event Processing")
        simulate_delay(2)
        
        # Now ClaimLens calls ClaimCenter APIs to get detailed data
        print_step(2, "Retrieve Structured Data - Claim Details")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}")
        self.retrieved_data['claim'] = response.json()
        print_response(response, "Claim Details")
        simulate_delay(1)
        
        print_step(3, "Retrieve Policy Information")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/{self.claim_id}/policy")
        self.retrieved_data['policy'] = response.json()
        print_response(response, "Policy Information")
        simulate_delay(1)
        
        print_step(4, "Retrieve Policy Coverages")
        response = requests.get(f"{CLAIMCENTER_URL}/claims/{self.claim_id}/policy/coverages")
        self.retrieved_data['coverages'] = response.json()
        print_response(response, "Policy Coverages")
        simulate_delay(1)
        
        print_step(5, "Retrieve Injury Incidents")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/{self.claim_id}/injury-incidents")
        self.retrieved_data['incidents'] = response.json()
        print_response(response, "Injury Incidents")
        simulate_delay(1)
        
        print_step(6, "Retrieve Semi-Structured Data - Documents")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/documents")
        self.retrieved_data['documents'] = response.json()
        print_response(response, "Document Metadata")
        
        # Get document content (base64 encoded)
        if self.retrieved_data['documents']:
            doc_id = self.retrieved_data['documents'][0]['document_id']
            response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/documents/{doc_id}/content")
            if response.status_code == 200:
                doc_content = response.json()
                decoded_content = base64.b64decode(doc_content['content_base64']).decode()
                print(f"📄 Document Content Preview: {decoded_content[:100]}...")
        simulate_delay(1)
        
        print_step(7, "Retrieve Notes and Activities")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/notes")
        self.retrieved_data['notes'] = response.json()
        print_response(response, "Existing Notes")
        
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/activities")
        self.retrieved_data['activities'] = response.json()
        print_response(response, "Existing Activities")
        simulate_delay(2)

    def phase_3_ai_analysis(self):
        """Phase 3: Simulate AI analysis in ClaimLens Engine"""
        print_section("PHASE 3: AI Analysis in ClaimLens Engine")
        print("🧠 ClaimLens AI Engine processes all retrieved data...")
        
        print_step(1, "Data Ingestion & Indexing")
        print("📊 Processing structured, semi-structured, and unstructured data:")
        print(f"   • Claim Type: {self.retrieved_data['claim']['description']}")
        print(f"   • Policy Type: {self.retrieved_data['policy']['policy_type']}")
        print(f"   • Number of Documents: {len(self.retrieved_data['documents'])}")
        print(f"   • Number of Coverages: {len(self.retrieved_data['coverages'])}")
        print("   • Indexing documents in AWS OpenSearch...")
        print("   • Storing metadata in AWS RDS...")
        simulate_delay(3)
        
        print_step(2, "AI Analysis Processing")
        print("🔍 Analyzing claim complexity and risk characteristics...")
        
        # Simulate comprehensive AI analysis
        self.ai_analysis_results = {
            "claim_id": self.claim_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "risk_assessment": {
                "overall_risk_score": 8.5,
                "complexity_level": "High",
                "fraud_indicators": ["Inconsistent injury description", "Late reporting"],
                "severity_indicators": ["Multiple body parts affected", "Extended treatment period"]
            },
            "coverage_analysis": {
                "coverage_adequacy": "Adequate",
                "potential_gaps": ["Rental car coverage may be insufficient"],
                "coverage_recommendations": ["Review medical payment limits"]
            },
            "medical_analysis": {
                "injury_severity": "Moderate to Severe",
                "treatment_consistency": "Consistent with reported injuries",
                "icd10_recommendations": [
                    {"code": "M54.5", "description": "Low back pain"},
                    {"code": "S13.4", "description": "Sprain of ligaments of cervical spine"}
                ]
            },
            "document_analysis": {
                "key_findings": [
                    "Medical records indicate pre-existing condition",
                    "Police report shows clear liability",
                    "Treatment plan is reasonable and necessary"
                ],
                "missing_documents": ["Updated medical records", "Work status report"],
                "document_quality": "Good"
            },
            "recommended_actions": [
                {
                    "priority": "High",
                    "action": "Request updated medical records from treating physician",
                    "reason": "Current records are 30+ days old"
                },
                {
                    "priority": "Medium", 
                    "action": "Schedule independent medical examination",
                    "reason": "Verify extent of ongoing treatment needs"
                },
                {
                    "priority": "Medium",
                    "action": "Review rental car usage and extend coverage if needed",
                    "reason": "Current usage approaching policy limits"
                }
            ],
            "estimated_reserve": {
                "medical": 75000,
                "indemnity": 25000,
                "total": 100000,
                "confidence": 0.78
            }
        }
        
        print("✅ AI Analysis Complete:")
        print(json.dumps(self.ai_analysis_results, indent=2))
        simulate_delay(2)

    def phase_4_write_results_back(self):
        """Phase 4: ClaimLens writes analysis results back to ClaimCenter"""
        print_section("PHASE 4: Writing AI Results Back to ClaimCenter")
        print("📝 ClaimLens writes analysis results back to ClaimCenter...")
        
        print_step(1, "Create High-Priority Activities")
        for i, action in enumerate(self.ai_analysis_results['recommended_actions']):
            activity_payload = {
                "activity_type": "AI_Recommendation",
                "description": f"[{action['priority']} Priority] {action['action']} - {action['reason']}",
                "assigned_user": "adjuster@insurance.com",
                "status": "Open"
            }
            
            response = requests.post(
                f"{CLAIMLENS_URL}/claim/v1/claims/{self.claim_id}/activities",
                json=activity_payload,
                headers={"Content-Type": "application/json"}
            )
            print_response(response, f"Activity {i+1} Created")
            simulate_delay(1)
        
        print_step(2, "Add AI Analysis Summary Note")
        summary_note = f"""
AI ANALYSIS SUMMARY (Risk Score: {self.ai_analysis_results['risk_assessment']['overall_risk_score']}/10)

COMPLEXITY: {self.ai_analysis_results['risk_assessment']['complexity_level']}

KEY FINDINGS:
- {chr(10).join('• ' + finding for finding in self.ai_analysis_results['document_analysis']['key_findings'])}

RISK INDICATORS:
- Fraud Indicators: {', '.join(self.ai_analysis_results['risk_assessment']['fraud_indicators'])}
- Severity Indicators: {', '.join(self.ai_analysis_results['risk_assessment']['severity_indicators'])}

ESTIMATED TOTAL RESERVE: ${self.ai_analysis_results['estimated_reserve']['total']:,}
(Confidence: {self.ai_analysis_results['estimated_reserve']['confidence']*100:.0f}%)

NEXT STEPS: {len(self.ai_analysis_results['recommended_actions'])} high-priority actions created.
        """.strip()
        
        note_payload = {
            "content": summary_note,
            "note_type": "AI_Analysis_Summary",
            "created_by": "ClaimLens_AI_Engine"
        }
        
        response = requests.post(
            f"{CLAIMLENS_URL}/claim/v1/claims/{self.claim_id}/notes",
            json=note_payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "AI Summary Note Created")
        simulate_delay(1)
        
        print_step(3, "Upload AI-Generated Summary Document")
        # Create a PDF summary document (simulated)
        pdf_summary = f"""
CLAIMLENS AI ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Claim: {self.retrieved_data['claim']['claim_number']}

EXECUTIVE SUMMARY:
This claim has been analyzed by ClaimLens AI and assigned a risk score of {self.ai_analysis_results['risk_assessment']['overall_risk_score']}/10.
The claim complexity is rated as {self.ai_analysis_results['risk_assessment']['complexity_level']}.

DETAILED ANALYSIS:
[Full AI analysis report would be included here]

RECOMMENDATIONS:
{chr(10).join(f"{i+1}. {action['action']}" for i, action in enumerate(self.ai_analysis_results['recommended_actions']))}
        """.strip()
        
        pdf_base64 = base64.b64encode(pdf_summary.encode()).decode()
        
        document_payload = {
            "filename": f"ClaimLens_AI_Summary_{self.claim_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
            "content_type": "application/pdf",
            "size": len(pdf_summary),
            "content_base64": pdf_base64
        }
        
        response = requests.post(
            f"{CLAIMLENS_URL}/claim/v1/claims/{self.claim_id}/documents",
            json=document_payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "AI Summary Document Uploaded")
        simulate_delay(1)
        
        print_step(4, "Update Medical Diagnoses with ICD-10 Codes")
        # First, we need to get injury incidents to update diagnoses
        if self.retrieved_data['incidents']:
            incident_id = self.retrieved_data['incidents'][0]['incident_id']
            
            for icd_rec in self.ai_analysis_results['medical_analysis']['icd10_recommendations']:
                diagnosis_payload = {
                    "icd10_code": icd_rec['code'],
                    "description": f"AI-Identified: {icd_rec['description']}",
                }
                
                response = requests.post(
                    f"{CLAIMLENS_URL}/claim/v1/claims/{self.claim_id}/injury-incidents/{incident_id}/medical-diagnoses",
                    json=diagnosis_payload,
                    headers={"Content-Type": "application/json"}
                )
                print_response(response, f"Medical Diagnosis Created - {icd_rec['code']}")
                simulate_delay(1)

    def phase_5_verification(self):
        """Phase 5: Verify all results were written back correctly"""
        print_section("PHASE 5: Verification & Results")
        print("🔍 Verifying all AI analysis results were properly written to ClaimCenter...")
        
        print_step(1, "Verify Created Activities")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/activities")
        activities = response.json()
        ai_activities = [act for act in activities if act['activity_type'] == 'AI_Recommendation']
        print(f"✅ Found {len(ai_activities)} AI-generated activities")
        for act in ai_activities[-3:]:  # Show last 3
            print(f"   📋 {act['activity_type']}: {act['description'][:80]}...")
        simulate_delay(1)
        
        print_step(2, "Verify AI Analysis Notes")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/notes")
        notes = response.json()
        ai_notes = [note for note in notes if 'AI' in note['note_type']]
        print(f"✅ Found {len(ai_notes)} AI-generated notes")
        for note in ai_notes:
            print(f"   📝 {note['note_type']}: {note['content'][:80]}...")
        simulate_delay(1)
        
        print_step(3, "Verify Uploaded Documents")
        response = requests.get(f"{CLAIMCENTER_URL}/claim/v1/claims/{self.claim_id}/documents")
        documents = response.json()
        ai_docs = [doc for doc in documents if 'ClaimLens' in doc['filename']]
        print(f"✅ Found {len(ai_docs)} AI-generated documents")
        for doc in ai_docs:
            print(f"   📄 {doc['filename']} ({doc['size']} bytes)")
        simulate_delay(1)
        
        print_step(4, "Integration Flow Summary")
        print("📊 INTEGRATION FLOW COMPLETED SUCCESSFULLY:")
        print("   1. ✅ Claim event triggered from ClaimCenter")
        print("   2. ✅ Event received by ClaimLens via EventBridge/API Gateway")
        print("   3. ✅ ClaimLens retrieved comprehensive claim data")
        print("   4. ✅ AI analysis performed on all data types")
        print("   5. ✅ Results written back to ClaimCenter via APIs")
        print("   6. ✅ Adjuster can now see AI insights in ClaimCenter UI")
        
        print(f"\n📈 FINAL ANALYSIS METRICS:")
        print(f"   • Risk Score: {self.ai_analysis_results['risk_assessment']['overall_risk_score']}/10")
        print(f"   • Complexity: {self.ai_analysis_results['risk_assessment']['complexity_level']}")
        print(f"   • Recommended Actions: {len(self.ai_analysis_results['recommended_actions'])}")
        print(f"   • Estimated Reserve: ${self.ai_analysis_results['estimated_reserve']['total']:,}")

def main():
    """Main demo execution"""
    print("🚀 Starting ClaimCenter & ClaimLens Integration Demo")
    print("📋 Make sure the mock server is running on http://localhost:5000")
    
    try:
        # Test server connectivity
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            raise Exception("Server not responding correctly")
            
        print("✅ Mock server is running and ready")
        
        # Run the demo
        demo = ClaimLensIntegrationDemo()
        demo.run_complete_demo()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to mock server")
        print("   Please make sure the server is running: python app.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()