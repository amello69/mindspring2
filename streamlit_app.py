import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# Load / save functions omitted for brevity here

# Ensure input state exists
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

user_input = st.text_area("Ask your tutor anything:", key="user_input")

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
            st.write(f"🤖 **Tutor:** {answer}")

            tokens_used = response.usage.total_tokens
            tokens_data[username] -= tokens_used
            save_tokens(tokens_data)
            st.success(f"Tokens used: {tokens_used}. Remaining: {tokens_data[username]}")

            # ✅ clear the input
            st.session_state["user_input"] = ""
    else:
        st.warning("Please enter a question.")
