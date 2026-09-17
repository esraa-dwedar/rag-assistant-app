import streamlit as st
from api_client import query_rag_api, check_backend_health

st.set_page_config(page_title="DevOps RAG Assistant", page_icon="🛠️", layout="wide")

st.title("🛠️ Cloud DevOps & Incident Assistant")
st.caption("Retrieval-Augmented Generation (RAG) system with grounded citations")

# Backend status check in sidebar
with st.sidebar:
    st.header("System Status")
    is_healthy = check_backend_health()
    if is_healthy:
        st.success("Backend: Online ✅")
    else:
        st.error("Backend: Offline ❌ (Start FastAPI on port 8000)")
    
    st.markdown("---")
    st.markdown("### Sample Questions")
    samples = [
        "What is the SLA response time for Sev-1 incidents?",
        "What should I do if a pod is in CrashLoopBackOff?",
        "How do I trigger manual PostgreSQL failover?",
        "What exit code indicates OOMKilled?"
    ]
    for sample in samples:
        if st.button(sample, use_container_width=True):
            st.session_state["prefill"] = sample

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            st.caption(f"📚 **Sources:** {', '.join(msg['sources'])}")

# User input
user_query = st.chat_input("Ask a question about Kubernetes, PostgreSQL failover, or incident SLAs...")
if "prefill" in st.session_state and st.session_state["prefill"]:
    user_query = st.session_state.pop("prefill")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant context and generating grounded answer..."):
            data, error = query_rag_api(user_query)
            if error:
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {error}"})
            else:
                answer = data.get("answer", "")
                sources = data.get("sources", [])
                st.markdown(answer)
                if sources:
                    st.caption(f"📚 **Sources:** {', '.join(sources)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })