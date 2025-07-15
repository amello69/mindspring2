import streamlit as st
from openai import OpenAI
import os

# --- Setup OpenAI client ---
client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# --- Helper to load & save user tokens ---
if not os.path.exists("user_tokens.txt"):
    with open("user_tokens.txt", "w") as f:
        pass

def load_tokens():
    tokens = {}
    with open("user_tokens.txt", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) == 2:
                tokens[parts[0]] = int(parts[1])
    return tokens

def save_tokens(tokens):
    with open("user_tokens.txt", "w") as f:
        for user, token_count in tokens.items():
            f.write(f"{user}:{token_count}\n")

# --- UI ---
st.image("logo.png", width=200)
st.title("🗣️ Science Tutor")

username = st.text_input("Enter your username:")

if username:
    tokens_data = load_tokens()
    if username not in tokens_data:
        tokens_data[username] = 1000
        save_tokens(tokens_data)

    tokens_remaining = tokens_data[username]
    st.subheader(f"Hello, {username}!")
    st.markdown(f"**Tokens remaining:** {tokens_remaining}")

    if tokens_remaining <= 0:
        st.error("You have used up all your tokens. Please purchase more to continue.")
    else:
        user_input = st.text_area("Ask your tutor anything:")

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
            else:
                st.warning("Please enter a question.")
else:
    st.info("Please enter your username to begin.")
