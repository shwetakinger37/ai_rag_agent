import uuid

import requests
import streamlit as st

DEFAULT_API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="AI RAG Agent Chatbot", page_icon="💬", layout="centered")
st.title("AI RAG Agent Chatbot")
st.caption("Upload a document and ask questions using RAG with tool support.")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("Backend API URL", value=DEFAULT_API_URL)
    use_rag = st.toggle("Use document context", value=True)

    st.divider()
    st.subheader("Document Upload")
    uploaded_file = st.file_uploader("Choose a PDF, TXT, or MD file", type=["pdf", "txt", "md"])

    if uploaded_file and st.button("Upload and Index"):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(f"{api_url}/upload", files=files, timeout=120)
            response.raise_for_status()
            data = response.json()
            st.success(f"Indexed {data['filename']} ({data['chunks_created']} chunks)")
        except Exception as exc:
            st.error(f"Upload failed: {exc}")

    if st.button("Start New Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

for chat_message in st.session_state.messages:
    with st.chat_message(chat_message["role"]):
        st.markdown(chat_message["content"])

user_message = st.chat_input("Ask a question about the uploaded document...")

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        answer = ""

        try:
            payload = {
                "session_id": st.session_state.session_id,
                "message": user_message,
                "use_rag": use_rag,
            }
            with requests.post(f"{api_url}/chat/stream", json=payload, stream=True, timeout=180) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        answer += chunk
                        placeholder.markdown(answer + "▌")
                placeholder.markdown(answer)
        except Exception as exc:
            answer = f"Error: {exc}"
            placeholder.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
