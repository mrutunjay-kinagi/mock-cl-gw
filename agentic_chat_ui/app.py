import streamlit as st
import requests

MCP_ENDPOINT = "http://mcp:8002/orchestrate"

st.set_page_config(page_title="ClaimLens Agentic Chat", layout="centered")
st.title("🤖 ClaimLens Agentic Chat")
st.caption("Query your claims using agentic AI powered by MCP")

prompt = st.text_input("Ask a question about the claim", placeholder="e.g. What are the endorsements on this policy?")
claim_id = st.text_input("Claim ID", value="claim_1")

if st.button("Submit"):
    if not prompt or not claim_id:
        st.error("Please enter both prompt and claim ID.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    MCP_ENDPOINT,
                    json={"prompt": prompt, "claim_id": claim_id},
                    timeout=15
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("AI Response Received")

                    st.markdown("### 🧠 Actions Executed")
                    for step in result.get("steps_executed", []):
                        st.markdown(f"- {step}")

                    st.markdown("### 📊 Details")
                    for entry in result.get("results", []):
                        st.subheader(entry.get("step"))
                        if "data" in entry:
                            st.json(entry["data"])
                        elif "message" in entry:
                            st.warning(entry["message"])

                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to MCP: {e}")
