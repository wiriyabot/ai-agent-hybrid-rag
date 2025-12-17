import streamlit as st
from src.graph import agent_app

st.set_page_config(page_title="AI Enterprise Analyst", page_icon="🤖", layout="centered")
st.title("🤖 AI Enterprise Analyst Agent")
st.caption("Architecture: Modular Hybrid RAG (SQL + Vector)")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Control Panel")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("This project is for educational purposes only.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ถามยอดขายหรือความคิดเห็นลูกค้า..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.status("🤖 Processing...", expanded=True) as status:
            inputs = {"question": prompt, "steps": []}
            final_res = None
            
            for output in agent_app.stream(inputs):
                for key, value in output.items():
                    if "final_answer" in value:
                        final_res = value["final_answer"]

            status.update(label="Complete", state="complete", expanded=False)
        
        if final_res:
            message_placeholder.markdown(final_res)
            st.session_state.messages.append({"role": "assistant", "content": final_res})