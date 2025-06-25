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
                    # Format AI response
                    ai_message = ""
                    if "steps_executed" in result:
                        ai_message += "### 🧠 Actions Executed\n"
                        for step in result.get("steps_executed", []):
                            ai_message += f"- {step}\n"
                    if "results" in result:
                        ai_message += "\n### 📊 Details\n"
                        for entry in result.get("results", []):
                            ai_message += f"**{entry.get('step', 'Step')}**\n"
                            if "data" in entry:
                                data = entry["data"]
                                if isinstance(data, dict):
                                    for k, v in data.items():
                                        ai_message += f"- **{k.replace('_', ' ').title()}**: {v}\n"
                                elif isinstance(data, list):
                                    for i, item in enumerate(data, start=1):
                                        ai_message += f"**Item {i}:**\n"
                                        if isinstance(item, dict):
                                            for k, v in item.items():
                                                ai_message += f"- **{k.replace('_', ' ').title()}**: {v}\n"
                                        else:
                                            ai_message += f"- {item}\n"
                                else:
                                    ai_message += f"**{data}**\n"
                            elif "message" in entry:
                                ai_message += f":warning: {entry['message']}\n"
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