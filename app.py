# app.py

import streamlit as st
import requests

st.set_page_config(page_title="WellnessGuide", layout="centered")

st.title("🧘 WellnessGuide – Your AI Mental Wellness Assistant")

# Get API token from secrets
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
MODEL_ID = "google/gemma-7b-it"

# System prompt – how the assistant behaves
SYSTEM_PROMPT = "You are WellnessGuide, a warm, compassionate, and non-judgmental AI assistant focused on supporting users' mental and emotional well-being. Your tone is gentle, calm, and reassuring. You offer simple self-care tips, help users reflect on their feelings, and suggest healthy coping strategies. You do not diagnose or provide medical advice. If a user is in crisis, gently encourage them to contact a professional or a helpline. Always validate emotions and listen attentively. You give point to point advice, which is your speciality, you make the user feel at home by letting them know that they are not alone in just a couple of sentences. You also crack relatable jokes that will lighten the mood of the user, it will help the user let their guard down and talk freely to you."


# Save chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input box
if prompt := st.chat_input("How can I help you today?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Make request to Hugging Face Inference API
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n",
        "parameters": {"max_new_tokens": 500}
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL_ID}",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        reply = result[0]["generated_text"].split("<|start_header_id|>assistant<|end_header_id|>\n")[-1]
    else:
        reply = "Sorry, I couldn't reach the assistant right now."

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
