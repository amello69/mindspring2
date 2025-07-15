import streamlit as st
from openai import OpenAI

# Secure API key from .streamlit/secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

st.title("🗣️ Simple AI English Tutor")

# Input box
user_input = st.text_area("Ask your tutor anything:")

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            # Call OpenAI with no history
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
            st.write(f"🤖 **Tutor:** {answer}")

            # Estimate tokens based on word count
            tokens_used = len(user_input.split()) // 2 + len(answer.split()) // 2
            st.info(f"Estimated tokens used: {tokens_used}")
    else:
        st.warning("Please enter a question.")
