import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Mental Health Chatbot",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); }
.stChatMessage { background-color: rgba(255,255,255,0.05); border-radius: 15px; padding: 10px; }
.stChatInput input { background-color: #16213e; color: white; border-radius: 10px; }
.stButton button { background: linear-gradient(90deg, #00d2ff, #7b2ff7); color: white; border: none; border-radius: 10px; width: 100%; font-weight: bold; }
.stAlert { border-radius: 10px; }
h1, h2, h3, p { color: white; }
.mood-box { background: rgba(255,255,255,0.1); border-radius: 10px; padding: 10px; text-align: center; color: white; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are a strict Mental Health Support Assistant.
Your ONLY purpose is to help users with mental health topics including:
- Stress, anxiety, depression, loneliness, sadness
- Emotional support and coping strategies
- Breathing exercises and relaxation techniques
- Mental wellness tips and self care
- Crisis support and helpline information
- Sleep issues related to mental health
- Trauma, grief, and emotional pain
- Motivation and positive thinking

STRICT RULES:
- ONLY respond to mental health related questions
- If user asks ANYTHING unrelated (science, politics, sports, AI, technology, celebrities, general knowledge etc.)
  respond EXACTLY with: I am only able to assist with mental health and emotional wellness topics. Please feel free to share how you are feeling or any mental health concerns you have.
- NEVER answer general knowledge questions
- NEVER discuss politics, technology, sports, entertainment or any other topic
- Respond in the same language as the user (English, Urdu or Sindhi)
- Always be kind, warm, empathetic and non-judgmental
- Keep responses clear, helpful and supportive
- If user is in crisis suggest professional help immediately"""

def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", None)
    if not api_key:
        st.error("API key not found! Please add GROQ_API_KEY in Streamlit secrets.")
        st.stop()
    return Groq(api_key=api_key)

def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["anxious", "anxiety", "nervous", "worried", "panic", "گھبراہٹ", "پریشان"]):
        return "Anxiety Detected"
    elif any(w in text for w in ["depressed", "depression", "hopeless", "empty", "worthless", "اداس", "مایوس"]):
        return "Depression Detected"
    elif any(w in text for w in ["lonely", "alone", "isolated", "no one", "اکیلا", "تنہا"]):
        return "Loneliness Detected"
    elif any(w in text for w in ["stress", "stressed", "overwhelmed", "pressure", "tired", "تھکا", "پریشانی"]):
        return "Stress Detected"
    elif any(w in text for w in ["happy", "good", "great", "better", "wonderful", "خوش", "اچھا"]):
        return "Positive Mood"
    elif any(w in text for w in ["angry", "rage", "furious", "frustrated", "غصہ"]):
        return " Anger Detected"
    elif any(w in text for w in ["scared", "fear", "afraid", "terrified", "ڈر"]):
        return "Fear Detected"
    else:
        return "Neutral"

def detect_crisis(text):
    text = text.lower()
    crisis_words = [
        "suicide", "kill myself", "end my life", "want to die",
        "self harm", "hurt myself", "no reason to live",
        "خودکشی", "مرنا چاہتا", "زندگی ختم", "مر جانا"
    ]
    return any(w in text for w in crisis_words)

def chat_with_ai(client, user_message):
    st.session_state.history.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.history,
        max_tokens=500,
        temperature=0.7
    )
    reply = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": reply})
    return reply

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("<h1 style='text-align:center;'>Mental Health Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#aaa;'>Powered by AI — English | اردو | سنڌي</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00d2ff;font-size:13px;'>Mood Detection | Crisis Support | Multilingual</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Breathing Exercise"):
        breathe_msg = """Box Breathing Exercise:

   Inhale slowly... 1, 2, 3, 4
   Hold your breath... 1, 2, 3, 4
   Exhale slowly... 1, 2, 3, 4
   Hold again... 1, 2, 3, 4

Repeat this 3-4 times. This technique reduces anxiety and stress instantly! """
        st.session_state.messages.append({"role": "assistant", "content": breathe_msg})
        st.rerun()

with col2:
    if st.button("Daily Wellness Tip"):
        tip_msg = """Daily Wellness Tip:

Take 5 minutes today to practice gratitude. Write down 3 things you are thankful for. Research shows this simple habit can significantly improve your mental wellbeing and reduce symptoms of depression and anxiety. 🌟"""
        st.session_state.messages.append({"role": "assistant", "content": tip_msg})
        st.rerun()

with col3:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

st.markdown("---")

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("Welcome! I am your AI Mental Health Assistant.\n\nI am here to listen and support you. You can talk to me in **English**, **Urdu (اردو)**, or **Sindhi (سنڌي)**.\n\nHow are you feeling today? 💙")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Share how you are feeling... (English, Urdu or Sindhi)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    mood = detect_mood(user_input)
    st.info("Current Mood: " + mood)

    if detect_crisis(user_input):
        crisis_response = """I am very concerned about you right now.

Please reach out for immediate help:
Pakistan Crisis Helpline: 0311-7786264
Umang Helpline: 0317-4288665
Rozan Counseling: 051-2890505

Please talk to someone you trust immediately. You are NOT alone. Help is available. """
        st.session_state.messages.append({"role": "assistant", "content": crisis_response})
    else:
        client = get_client()
        response = chat_with_ai(client, user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()

st.markdown("---")
st.markdown("<p style='text-align:center;color:#555;font-size:12px;'>This chatbot provides emotional support only and is not a substitute for professional mental health care.</p>", unsafe_allow_html=True)
