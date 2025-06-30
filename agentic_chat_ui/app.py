import streamlit as st
import requests

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

MCP_ENDPOINT = "http://mcp:8002/orchestrate"

st.set_page_config(page_title="Claim Agentic Chat", layout="centered")
st.title("🤖 Claims Agentic Chat")
st.caption("Query your claims using agentic AI powered by MCP")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

prompt = st.text_input("Ask a question about the claim", placeholder="e.g. Fetch policy details for this claim", key="user_input")
claim_id = st.text_input("Claim ID", value="claim_1", key="claim_id_input")

if st.button("Submit"):
    if not prompt or not claim_id:
        st.error("Please enter both prompt and claim ID.")
    else:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    MCP_ENDPOINT,
                    json={"prompt": prompt, "claim_id": claim_id},
                    timeout=15
                )
                if response.status_code == 200:
                    result = response.json()
                    print(f"Response from MCP: {result}")
                    ai_message = ""

                    # Format Actions Executed
                    if "steps_executed" in result:
                        ai_message += "### 🧠 Actions Executed\n"
                        for step in result.get("steps_executed", []):
                            ai_message += f"- {step}\n"

                    # Format Results
                    if "results" in result:
                        ai_message += "\n### 📊 Details\n"
                        for entry in result.get("results", []):
                            step_name = entry.get("step", "Step")
                            ai_message += f"\n**{step_name}**\n"

                            if "data" in entry:
                                data = entry["data"]

                                # Dynamically format data based on step
                                if step_name == "Claim retrieved":
                                    ai_message += "\n**Claim Details:**\n"
                                    ai_message += f"- **Claim ID:** {data.get('claim_id', 'N/A')}\n"
                                    ai_message += f"- **Claim Number:** {data.get('claim_number', 'N/A')}\n"
                                    ai_message += f"- **Description:** {data.get('description', 'N/A')}\n"
                                    ai_message += f"- **Loss Date:** {data.get('loss_date', 'N/A')}\n"
                                    ai_message += f"- **Status:** {data.get('status', 'N/A')}\n"
                                    ai_message += f"- **Policy ID:** {data.get('policy_id', 'N/A')}\n"

                                    # Format Accident Details
                                    accident_details = data.get("accident_details", {})
                                    if accident_details:
                                        ai_message += "\n**Accident Details:**\n"
                                        location = accident_details.get("location", {})
                                        ai_message += f"- **Location:** {location.get('street', 'N/A')}, {location.get('city', 'N/A')}, {location.get('state', 'N/A')} {location.get('zip_code', 'N/A')}\n"
                                        ai_message += f"- **Damage Estimate:** ${accident_details.get('damage_estimate', 'N/A')}\n"
                                        injuries = accident_details.get("injuries", [])
                                        if injuries:
                                            ai_message += "\n**Injuries:**\n"
                                            for injury in injuries:
                                                ai_message += f"  - **Name:** {injury.get('name', 'N/A')}, **Type:** {injury.get('type', 'N/A')}, **Severity:** {injury.get('severity', 'N/A')}\n"

                                elif step_name == "Policy details fetched":
                                    ai_message += "\n**Policy Details:**\n"
                                    ai_message += f"- **Policy ID:** {data.get('policy_id', 'N/A')}\n"
                                    ai_message += f"- **Policy Number:** {data.get('policy_number', 'N/A')}\n"
                                    ai_message += f"- **LOB:** {data.get('lob', 'N/A')}\n"
                                    ai_message += f"- **Policyholder Name:** {data.get('policyholder_name', 'N/A')}\n"
                                    ai_message += f"- **Status:** {data.get('status', 'N/A')}\n"

                                elif step_name == "Policy coverages fetched":
                                    ai_message += "\n**Coverages:**\n"
                                    for coverage in data:
                                        ai_message += f"- {coverage}\n"

                                elif step_name == "Policy endorsements fetched":
                                    ai_message += "\n**Endorsements:**\n"
                                    for endorsement in data:
                                        ai_message += f"- **Code:** {endorsement.get('code', 'N/A')}, **Title:** {endorsement.get('title', 'N/A')}\n"

                                elif step_name == "Documents retrieved":
                                    ai_message += "\n**Documents:**\n"
                                    for document in data:
                                        ai_message += f"- **Filename:** {document.get('filename', 'N/A')}, **Content Type:** {document.get('content_type', 'N/A')}\n"

                                elif step_name == "Injuries retrieved":
                                    ai_message += "\n**Injuries:**\n"
                                    for injury in data:
                                        ai_message += f"- **Description:** {injury.get('description', 'N/A')}, **Severity:** {injury.get('severity', 'N/A')}, **Body Parts:** {', '.join(injury.get('body_parts', []) or ['N/A'])}\n"

                            elif "message" in entry:
                                ai_message += f"\n:warning: {entry['message']}\n"

                    st.session_state.chat_history.append({"role": "ai", "content": ai_message})
                else:
                    st.session_state.chat_history.append({"role": "ai", "content": f":x: Error: {response.status_code} - {response.text}"})
            except Exception as e:
                st.session_state.chat_history.append({"role": "ai", "content": f":x: Failed to connect to MCP: {e}"})

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='background:#4B8BBE;color:white;padding:10px 16px;border-radius:12px;margin-bottom:8px;max-width:80%;align-self:flex-end;text-align:right;'>
                <b>You:</b> {msg['content']}
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='background:#f0f2f6;color:#22314a;padding:10px 16px;border-radius:12px;margin-bottom:8px;max-width:80%;'>
                <b>AI:</b><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True
        )