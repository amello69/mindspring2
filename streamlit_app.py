import streamlit as st
from openai import OpenAI
import os

# Load OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# Load or create user_tokens.txt
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

# --- Ensure input state exists for clearing later ---
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# --- UI: Logo & Title ---
st.image("logo.png", width=200)
st.title("🗣️ English Tutor")

# --- Username input ---
username = st.text_input("Enter your username:")

if username:
    tokens_data = load_tokens()
    if username not in tokens_data:
        tokens_data[username] = 1000
        save_tokens(tokens_data)

    tokens_remaining = tokens_data[username]

    st.subheader(f"Hello, {username}!")
    st.markdown(f"**Tokens remaining:** {tokens_remaining}")

    # --- If out of tokens ---
    if tokens_remaining <= 0:
        st.error("You have used up all your tokens. Please purchase more to continue.")
    else:
        # --- Ask the tutor ---
        user_input = st.text_area("Ask your tutor anything:", key="user_input")

        if st.button("Submit"):
            if user_input.strip():
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4.1-nano",
                        messages=[
                            {"
