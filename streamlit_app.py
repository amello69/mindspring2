import streamlit as st
from openai import OpenAI

# Secure API key from .streamlit/secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# --- Initialize state ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "tokens_remaining" not in st.session_state:
    st.session_state["tokens_remaining"] = 1000  # start monthly quota

st.title("🗣️ Simple AI English Tutor")

# --- Show tokens info ---
st.sidebar.markdown(f"**Tokens remaining:** {st.session_state['tokens_remaining']}")

# --- Display chat history ---
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.write(f"📝 **You:** {chat['content']}")
    else:
        st.write(f"🤖 **Tutor:** {chat['content']}")

# --- Input & submit ---
disable_input = st.session_state["tokens_remaining"] <= 0
if disable_input:
    st.error("You have exhausted your monthly tokens. Please purchase more to continue.")

user_input = st.text_area("Ask your tutor anything:", disabled=disable_input)

if st.button("Submit", disabled=disable_input):
    if user_input.strip():
        with st.spinner("Thinking..."):
            # Build minimal context
            messages = [{"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."}]
            for past in st.session_state["chat_history"]:
                messages.append({"role": past["role"], "content": past["content"]})
            messages.append({"role": "user", "content": user_input})

            # Call OpenAI
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages
            )
            answer = response.choices[0].message.content

            # Update history
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})

            # Show immediate response
            st.write(f"🤖 **Tutor:** {answer}")

            # Update tokens
            tokens_used = len(user_input.split()) // 2 + len(answer.split()) // 2
            st.session_state["tokens_remaining"] -= tokens_used
            st.success(f"Tokens used: {tokens_used}. Remaining: {st.session_state['tokens_remaining']}")
    else:
        st.warning("Please enter a question.")
