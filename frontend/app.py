# import streamlit as st
# import requests

# API_URL = "http://localhost:8000/ask"

# st.title("GenAI Medical Advisor")
# st.write("Ask any medical question. The advisor will respond based on the provided medical book.")

# user_input = st.text_input("Your question:")

# if st.button("Ask"):
#     if user_input:
#         with st.spinner("Thinking..."):
#             response = requests.post(API_URL, json={"question": user_input})
#             if response.ok:
#                 data = response.json()
#                 st.markdown(f"**Answer:** {data['answer']}")
#                 st.markdown("**Sources:**")
#                 for src in data["sources"]:
#                     st.code(src)
#             else:
#                 st.error("Error from backend.")
import streamlit as st
import requests

st.set_page_config(page_title="🩺 GenAI Medical Advisor", layout="wide")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

API_URL = "http://localhost:8000/ask"

# Sidebar
with st.sidebar:
    st.title("🩺 GenAI Medical Advisor")
    st.markdown("""
    **Ask any medical question and get solutions .**
    """)
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
    st.markdown("---")
    feedback = st.text_area("💬 Feedback or suggestions:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Persistent chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main area: show welcome card if chat is empty
if not st.session_state.messages:
    # Centered welcome card
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh;">
            <img src="https://img.icons8.com/fluency/96/medical-doctor.png" width="96" />
            <h1 style="margin-bottom: 0;">Welcome to GenAI Medical Advisor</h1>
            <p style="font-size: 1.2em; color: #aaa; max-width: 480px; text-align: center;">
                This assistant provides solutions and precautions for your medical questions.
                <br><br>
                <b>Type your question below to begin.</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display chat history
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input at the bottom
prompt = st.chat_input("Type your medical question here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Prepare last 10 messages for context
    history_to_send = st.session_state.messages[-10:]

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("Thinking..."):
            try:
                history_dicts = [{"role": m["role"], "content": m["content"]} for m in history_to_send]
                response = requests.post(API_URL, json={"question": prompt, "history": history_dicts}, timeout=60)
                if response.ok:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    st.markdown(answer)
                    if sources:
                        with st.expander("📚 Sources consulted"):
                            for i, src in enumerate(sources, 1):
                                st.markdown(f"**Source {i}:** {src}")
                else:
                    st.error("❌ Error: Backend did not respond as expected.")
                    answer = "Sorry, I couldn't get an answer from the server."
            except Exception as e:
                st.error(f"❌ Error: {e}")
                answer = "Sorry, something went wrong."

    st.session_state.messages.append({"role": "assistant", "content": answer})
