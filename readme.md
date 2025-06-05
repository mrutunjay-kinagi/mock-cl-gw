# ClaimCenter & ClaimLens Mock APIs

A comprehensive mock implementation of Guidewire ClaimCenter and Doclens.ai ClaimLens APIs for integration testing and development. This project simulates the complete bidirectional data flow between ClaimCenter and ClaimLens, including event-driven claim processing, AI analysis, and data synchronization.

## 🎯 Overview

This mock system replicates the integration described in the ClaimLens documentation:

- **ClaimCenter APIs** - Mock Guidewire ClaimCenter endpoints for claims, policies, documents, notes, and activities
- **ClaimLens APIs** - Mock ClaimLens AI analysis service and webhook endpoints
- **Event System** - Simulated `Claim:Create` and `Claim:Update` event handling
- **Bidirectional Data Flow** - Complete integration between both systems

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the mock server:**
   ```bash
   python app.py
   ```

5. **Access the APIs:**
   - Base URL: `http://localhost:5000`
   - Health check: `http://localhost:5000/health`
   - API overview: `http://localhost:5000/`

## 📁 Project Structure

```
claimcenter_mock/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── models/                  # Data models
│   ├── __init__.py
│   ├── claim_models.py      # Claim, Activity, Note, Document models
│   └── policy_models.py     # Policy, Coverage, Endorsement models
├── routes/                  # API route handlers
│   ├── __init__.py
│   ├── claimcenter_routes.py # ClaimCenter API endpoints
│   └── claimlens_routes.py   # ClaimLens API endpoints
├── events/                  # Event handling
│   ├── __init__.py
│   └── event_handler.py     # Event creation and processing
└── utils/                   # Utilities
    ├── __init__.py
    └── sample_data.py       # Sample data generation
```

## 🔧 API Endpoints

### ClaimCenter APIs (Data Retrieval)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/claimcenter/claim/v1/claims/{claimId}` | Get claim details |
| GET | `/claimcenter/claim/{claimId}/policy` | Get policy information |
| GET | `/claimcenter/claims/{claimId}/policy/coverages` | Get policy coverages |
| GET | `/claimcenter/claims/{claimId}/policy/endorsements` | Get policy endorsements |
| GET | `/claimcenter/claim/{claimId}/injury-incidents` | Get injury incidents |
| GET | `/claimcenter/claim/v1/claims/{claimId}/documents` | Get claim documents |
| GET | `/claimcenter/claim/v1/claims/{claimId}/documents/{docId}/content` | Get document content |
| GET | `/claimcenter/claim/v1/claims/{claimId}/notes` | Get claim notes |
| GET | `/claimcenter/claim/v1/claims/{claimId}/activities` | Get claim activities |
| POST | `/claimcenter/claim/v1/claims/{claimId}/trigger-event` | Trigger claim events |

### ClaimLens APIs (AI Analysis & Data Writing)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/claimlens/webhook/claim-event` | Receive claim events |
| POST | `/api/claim/v1/claims/{claimId}/activities` | Create activities |
| POST | `/api/claim/v1/claims/{claimId}/notes` | Create notes |
| POST | `/api/claim/v1/claims/{claimId}/documents` | Upload documents |
| POST | `/api/claim/v1/claims/{claimId}/injury-incidents/{incidentId}/medical-diagnoses` | Create medical diagnoses |
| PATCH | `/api/claim/v1/claims/{claimId}/injury-incidents/{incidentId}/medical-diagnoses/{diagnosisId}` | Update medical diagnoses |
| GET | `/api/claimlens/chat/session` | Get chat session |
| POST | `/api/claimlens/chat/message` | Send chat message |

## 📊 Sample Data

The mock comes with pre-populated sample data:

### Claims
- **claim_1**: Auto accident with injuries (`sendToClaimLens: true`)
- **claim_2**: Property damage claim (`sendToClaimLens: false`)

### Policies
- **policy_1**: Auto insurance policy
- **policy_2**: Homeowners insurance policy

## 🧪 Testing Examples

### 1. Get Claim Information
```bash
curl http://localhost:5000/claimcenter/claim/v1/claims/claim_1
```

### 2. Trigger a Claim Event
```bash
curl -X POST http://localhost:5000/claimcenter/claim/v1/claims/claim_1/trigger-event \
  -H "Content-Type: application/json" \
  -d '{"event_type": "Claim:Update"}'
```

### 3. Simulate ClaimLens Processing Event
```bash
curl -X POST http://localhost:5000/api/claimlens/webhook/claim-event \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Claim:Create",
    "claim_id": "claim_1",
    "event_id": "evt_123"
  }'
```

### 4. Create Activity (ClaimLens → ClaimCenter)
```bash
curl -X POST http://localhost:5000/api/claim/v1/claims/claim_1/activities \
  -H "Content-Type: application/json" \
  -d '{
    "activity_type": "AI_Review",
    "description": "High-risk characteristics identified by AI analysis",
    "assigned_user": "adjuster@insurance.com"
  }'
```

### 5. Create AI-Generated Note
```bash
curl -X POST http://localhost:5000/api/claim/v1/claims/claim_1/notes \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI Analysis: Coverage mismatch detected. Recommend immediate review.",
    "note_type": "AI_Analysis",
    "created_by": "ClaimLens_AI"
  }'
```

### 6. Get Document Content (Base64 encoded)
```bash
curl http://localhost:5000/claimcenter/claim/v1/claims/claim_1/documents/doc_1/content
```

## 🔄 Integration Flow Simulation

### Complete Flow Example:

1. **Flag a Claim for AI Analysis:**
   - Claim has `sendToClaimLens: true`

2. **Trigger Event:**
   ```bash
   curl -X POST http://localhost:5000/claimcenter/claim/v1/claims/claim_1/trigger-event \
     -H "Content-Type: application/json" \
     -d '{"event_type": "Claim:Update"}'
   ```

3. **ClaimLens Receives Event:**
   - Event is automatically "sent" to ClaimLens webhook
   - AI processing simulation occurs

4. **ClaimLens Writes Back Results:**
   - Creates activities with risk analysis
   - Adds AI-generated notes
   - Updates medical diagnoses with ICD-10 codes

5. **Verify Results:**
   ```bash
   # Check created activities
   curl http://localhost:5000/claimcenter/claim/v1/claims/claim_1/activities
   
   # Check AI notes
   curl http://localhost:5000/claimcenter/claim/v1/claims/claim_1/notes
   ```

## 🎨 Key Features

### Event-Driven Architecture
- ✅ Simulates Guidewire Messaging (On-Prem)
- ✅ Simulates AWS EventBridge (Cloud)
- ✅ Configurable event triggering with `sendToClaimLens` flag

### Comprehensive Data Models
- ✅ Claims, Policies, Coverages, Endorsements
- ✅ Injury Incidents, Medical Diagnoses, Bodily Injury Points
- ✅ Documents, Notes, Activities
- ✅ No Pydantic dependency - uses Python dataclasses

### AI Analysis Simulation
- ✅ Risk scoring and complexity assessment
- ✅ Recommended actions generation
- ✅ Conversational chat interface
- ✅ Source citation tracking

### Bidirectional Integration
- ✅ ClaimCenter → ClaimLens data flow
- ✅ ClaimLens → ClaimCenter result writing
- ✅ Real-time event processing simulation

## 🔍 Monitoring & Debugging

### Console Output
The mock server provides detailed console output showing:
- Event triggering and routing
- API calls and responses
- AI processing simulation

### Health Check
```bash
curl http://localhost:5000/health
```

### API Discovery
```bash
curl http://localhost:5000/
```

## 🛠️ Customization

### Adding New Sample Data
Edit `utils/sample_data.py` to add more claims, policies, or documents.

### Modifying AI Responses
Update the AI analysis logic in `routes/claimlens_routes.py` in the `receive_claim_event` function.

### Adding New Endpoints
Add new routes to the appropriate blueprint files in the `routes/` directory.

## 🚫 What This Mock Doesn't Include

- Real AI/ML processing
- Authentication/Authorization (mocked)
- Database persistence (in-memory only)
- Real file storage
- Production-grade error handling
- Rate limiting or throttling

## 🔄 Development Workflow

1. **Start the server:** `python app.py`
2. **Make changes** to code files
3. **Restart server** to see changes (or use Flask's debug mode)
4. **Test endpoints** using curl or Postman
5. **Check console output** for event flow debugging

## 📝 Notes

- All data is stored in memory and resets when the server restarts
- Base64 document content is simulated with sample text
- Event timestamps and IDs are automatically generated
- The mock follows the API patterns described in the ClaimLens integration documentation

## 🤝 Contributing

This is a mock/testing project. Feel free to:
- Add more realistic sample data
- Implement additional API endpoints
- Enhance the AI analysis simulation
- Add more comprehensive error handling

## 📄 License

This project is for testing and development purposes. Use according to your organization's policies.