
import streamlit as st
from groq import Groq

API_KEY = "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"
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="Mental Health Chatbot", layout="centered")

st.markdown("""
<style>
body { background-color: #1a1a2e; }
.stApp { background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); }
.stTextInput input { background-color: #16213e; color: white; border-radius: 10px; }
.stButton button { background: linear-gradient(90deg, #00d2ff, #7b2ff7); color: white; border: none; border-radius: 10px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:white;'>Mental Health Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aaa;'>Powered by AI — English | Urdu | Sindhi</p>", unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["anxious","anxiety","nervous","worried","panic"]):
        return "Anxiety"
    elif any(w in text for w in ["depressed","hopeless","empty","worthless"]):
        return "Depression"
    elif any(w in text for w in ["lonely","alone","isolated"]):
        return "Loneliness"
    elif any(w in text for w in ["stress","stressed","overwhelmed","tired"]):
        return "Stress"
    elif any(w in text for w in ["happy","good","great","better"]):
        return "Positive"
    else:
        return "Neutral"

def detect_crisis(text):
    text = text.lower()
    crisis_words = ["suicide","kill myself","end my life","want to die","self harm","hurt myself"]
    return any(w in text for w in crisis_words)

def chat_with_ai(user_message):
    st.session_state.history.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a compassionate mental health assistant. Listen carefully and respond with empathy. Respond in the same language as the user (English, Urdu or Sindhi). Always be kind and non-judgmental."}
        ] + st.session_state.history
    )
    reply = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": reply})
    return reply

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("Welcome! I am your AI Mental Health Assistant. How are you feeling today?")

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Breathe"):
        breathe_msg = "Box Breathing Exercise: Inhale for 4 seconds... Hold for 4 seconds... Exhale for 4 seconds... Repeat 3-4 times!"
        st.session_state.messages.append({"role": "assistant", "content": breathe_msg})
        st.rerun()

user_input = st.chat_input("Type your message in English, Urdu or Sindhi...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    mood = detect_mood(user_input)
    st.info("Current Mood: " + mood)
    if detect_crisis(user_input):
        crisis_response = "I am very concerned about you. Please call Pakistan Crisis Helpline: 0311-7786264 or Umang Helpline: 0317-4288665 immediately. You are not alone!"
        st.session_state.messages.append({"role": "assistant", "content": crisis_response})
    else:
        response = chat_with_ai(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
