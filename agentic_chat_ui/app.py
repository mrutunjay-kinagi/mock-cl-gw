import streamlit as st
import requests

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


MCP_ENDPOINT = "http://mcp:8002/orchestrate"

st.set_page_config(page_title="ClaimLens Agentic Chat", layout="centered")
st.title("🤖 Claims Agentic Chat")
st.caption("Query your claims using agentic AI powered by MCP")

prompt = st.text_input("Ask a question about the claim", placeholder="e.g. Fetch policy details for this claim")
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
                        st.markdown(f"### ✅ {entry.get('step')}")
                        
                        if "data" in entry:
                            data = entry["data"]

                            if isinstance(data, dict):
                                for k, v in data.items():
                                    st.markdown(f"- **{k.replace('_', ' ').title()}**: {v}")
                            elif isinstance(data, list):
                                for i, item in enumerate(data, start=1):
                                    st.markdown(f"**Item {i}:**")
                                    if isinstance(item, dict):
                                        for k, v in item.items():
                                            st.markdown(f"- **{k.replace('_', ' ').title()}**: {v}")
                                    else:
                                        st.markdown(f"- {item}")
                            else:
                                st.markdown(f"**{data}**")

                        elif "message" in entry:
                            st.warning(entry["message"])


                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to MCP: {e}")
