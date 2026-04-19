import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="MindCare AI",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* { font-family: 'Poppins', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e, #16213e);
    border-right: 1px solid rgba(255,255,255,0.1);
}

section[data-testid="stSidebar"] * { color: white !important; }

.main-header {
    background: linear-gradient(135deg, #667eea, #764ba2, #f64f59);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 10px 40px rgba(102,126,234,0.4);
}

.main-header h1 { color: white !important; font-size: 2.5em; font-weight: 700; margin: 0; }
.main-header p { color: rgba(255,255,255,0.9) !important; font-size: 1em; margin: 10px 0 0 0; }

.badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 12px;
    margin: 5px 3px;
}

.mood-card {
    background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
    border: 1px solid rgba(102,126,234,0.4);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    color: white;
    margin: 10px 0;
}

.mood-card h3 { margin: 0; font-size: 1.5em; }
.mood-card p { margin: 5px 0 0 0; color: rgba(255,255,255,0.7); font-size: 0.85em; }

.stat-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    color: white;
    margin: 5px 0;
}

.stat-card h2 { margin: 0; color: #667eea; font-size: 2em; }
.stat-card p { margin: 5px 0 0 0; color: rgba(255,255,255,0.7); font-size: 0.8em; }

.stChatMessage {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 15px !important;
    margin: 5px 0 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

.stChatMessage p { color: white !important; }

.stButton button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    color: white !important;
}

.info-box {
    background: linear-gradient(135deg, rgba(0,210,255,0.15), rgba(123,47,247,0.15));
    border: 1px solid rgba(0,210,255,0.3);
    border-radius: 15px;
    padding: 15px;
    color: white;
    margin: 10px 0;
}

div[data-testid="stMarkdownContainer"] p { color: white; }
label { color: white !important; }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are a strict Mental Health Support Assistant named MindCare AI.
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
- If user asks ANYTHING unrelated respond EXACTLY with: I am only able to assist with mental health and emotional wellness topics. Please feel free to share how you are feeling or any mental health concerns you have.
- NEVER answer general knowledge questions
- NEVER discuss politics, technology, sports, entertainment or any other topic
- Respond in the same language as the user (English, Urdu or Sindhi)
- Always be kind, warm, empathetic and non-judgmental
- If user is in crisis suggest professional help immediately"""

def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", None)
    if not api_key:
        st.error("API key not found!")
        st.stop()
    return Groq(api_key=api_key)

def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["anxious","anxiety","nervous","worried","panic","گھبراہٹ","پریشان"]):
        return ("Anxiety", "#f093fb")
    elif any(w in text for w in ["depressed","depression","hopeless","empty","worthless","اداس","مایوس"]):
        return ("Depression", "#4facfe")
    elif any(w in text for w in ["lonely","alone","isolated","no one","اکیلا","تنہا"]):
        return ("Loneliness", "#43e97b")
    elif any(w in text for w in ["stress","stressed","overwhelmed","pressure","tired","تھکا","پریشانی"]):
        return ("Stress", "#f7971e")
    elif any(w in text for w in ["happy","good","great","better","wonderful","خوش","اچھا"]):
        return ("Positive", "#56ab2f")
    elif any(w in text for w in ["angry","rage","furious","frustrated","غصہ"]):
        return ("Anger", "#ff416c")
    elif any(w in text for w in ["scared","fear","afraid","terrified","ڈر"]):
        return ("Fear", "#a18cd1")
    else:
        return ("Neutral", "#667eea")

def detect_crisis(text):
    text = text.lower()
    crisis_words = ["suicide","kill myself","end my life","want to die","self harm","hurt myself","no reason to live","خودکشی","مرنا چاہتا","زندگی ختم"]
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
if "current_mood" not in st.session_state:
    st.session_state.current_mood = ("Neutral", "#667eea")
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

with st.sidebar:
    st.markdown("<h2 style='text-align:center;color:white;'>MindCare AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#aaa;font-size:12px;'>Your Mental Health Companion</p>", unsafe_allow_html=True)
    st.markdown("---")

    mood_name, mood_color = st.session_state.current_mood
    st.markdown(f"""
    <div class='mood-card'>
        <h4 style='color:{mood_color};margin:5px 0;'>{mood_name}</h4>
        <p>Current Mood</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <h2>{st.session_state.total_messages}</h2>
            <p>Messages</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <h2>{len(st.session_state.history)//2}</h2>
            <p>Exchanges</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:white;font-weight:600;'>Quick Actions</p>", unsafe_allow_html=True)

    if st.button("Breathing Exercise", use_container_width=True):
        breathe_msg = """**Box Breathing Exercise**

**Step 1:** Inhale slowly... 1, 2, 3, 4
**Step 2:** Hold your breath... 1, 2, 3, 4
**Step 3:** Exhale slowly... 1, 2, 3, 4
**Step 4:** Hold again... 1, 2, 3, 4

Repeat this **3-4 times**. This reduces anxiety instantly!"""
        st.session_state.messages.append({"role": "assistant", "content": breathe_msg})
        st.session_state.total_messages += 1
        st.rerun()

    if st.button("Daily Wellness Tip", use_container_width=True):
        tip_msg = """**Daily Wellness Tip**

Take **5 minutes** today to practice gratitude. Write down **3 things** you are thankful for.

Research shows this simple habit significantly improves mental wellbeing!"""
        st.session_state.messages.append({"role": "assistant", "content": tip_msg})
        st.session_state.total_messages += 1
        st.rerun()

    if st.button("Crisis Helplines", use_container_width=True):
        help_msg = """**Pakistan Mental Health Helplines**

Umang Helpline: 0317-4288665
Pakistan Crisis Line: 0311-7786264
Rozan Counseling: 051-2890505
Rescue: 1122

You are NOT alone. Help is always available!"""
        st.session_state.messages.append({"role": "assistant", "content": help_msg})
        st.session_state.total_messages += 1
        st.rerun()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.total_messages = 0
        st.session_state.current_mood = ("Neutral", "#667eea")
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div class='info-box'>
        <p style='font-size:12px;margin:0;'><b>Languages Supported</b></p>
        <p style='font-size:12px;margin:5px 0 0 0;'>English | Urdu | Sindhi</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color:#555;font-size:10px;text-align:center;margin-top:10px;'>Not a substitute for professional help</p>", unsafe_allow_html=True)

st.markdown("""
<div class='main-header'>
    <h1>MindCare AI</h1>
    <p>Your Compassionate Mental Health Companion</p>
    <div style='margin-top:15px;'>
        <span class='badge'>Mood Detection</span>
        <span class='badge'>Crisis Support</span>
        <span class='badge'>Multilingual</span>
        <span class='badge'>AI Powered</span>
        <span class='badge'>24/7 Available</span>
    </div>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("""**Welcome to MindCare AI!**

I am your compassionate AI Mental Health Assistant. I am here to listen, support, and guide you.

You can talk to me in **English**, **Urdu**, or **Sindhi**.

How are you feeling today?""")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Share how you are feeling... (English, Urdu or Sindhi)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.total_messages += 1

    mood_name, mood_color = detect_mood(user_input)
    st.session_state.current_mood = (mood_name, mood_color)

    if detect_crisis(user_input):
        crisis_response = """**I am very concerned about you right now.**

Please reach out for immediate help:

Pakistan Crisis Helpline: 0311-7786264
Umang Helpline: 0317-4288665
Rozan Counseling: 051-2890505

Please talk to someone you trust immediately. You are NOT alone. Help is available."""
        st.session_state.messages.append({"role": "assistant", "content": crisis_response})
    else:
        client = get_client()
        with st.spinner("MindCare AI is thinking..."):
            response = chat_with_ai(client, user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()
