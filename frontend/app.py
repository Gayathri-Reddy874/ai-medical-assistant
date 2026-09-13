import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="MediAssist AI",
    page_icon="⚕️",
    layout="wide",
)

# ---------- Pharma theme styling ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #F4F8F7 0%, #EDF3F1 100%);
    }

    /* Header */
    .mediassist-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 22px 28px;
        background: linear-gradient(90deg, #0B4F4A 0%, #0F6B63 100%);
        border-radius: 14px;
        margin-bottom: 28px;
        box-shadow: 0 4px 18px rgba(11, 79, 74, 0.18);
    }
    .mediassist-header .icon {
        font-size: 34px;
        background: rgba(255,255,255,0.15);
        padding: 10px 14px;
        border-radius: 12px;
    }
    .mediassist-header h1 {
        font-family: 'Source Serif 4', serif;
        color: #FFFFFF;
        font-size: 28px;
        margin: 0;
        letter-spacing: 0.2px;
    }
    .mediassist-header p {
        color: #CFE9E4;
        margin: 2px 0 0 0;
        font-size: 13.5px;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0B3B37;
    }
    section[data-testid="stSidebar"] * {
        color: #E7F3F1 !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: #C9A24B;
        color: #0B3B37 !important;
        border: none;
        font-weight: 600;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #DBB765;
    }

    /* Section subheader */
    .section-label {
        font-family: 'Source Serif 4', serif;
        color: #0B4F4A;
        font-size: 20px;
        border-bottom: 2px solid #C9A24B;
        display: inline-block;
        padding-bottom: 4px;
        margin-bottom: 18px;
    }

    /* Chat bubbles */
    .chat-row {
        margin-bottom: 16px;
    }
    .bubble-user {
        background: #FFFFFF;
        border-left: 4px solid #0F6B63;
        padding: 12px 16px;
        border-radius: 10px;
        color: #14332F;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 6px;
    }
    .bubble-ai {
        background: #0B4F4A;
        padding: 12px 16px;
        border-radius: 10px;
        color: #F2F8F6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .bubble-label {
        font-size: 11.5px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        opacity: 0.7;
        margin-bottom: 4px;
        display: block;
    }

    /* Input + primary button */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1.5px solid #B8D4CF !important;
        padding: 10px 12px !important;
    }
    div[data-testid="stForm"] button, .stButton > button {
        background: #0F6B63 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 8px 22px !important;
    }
    div[data-testid="stForm"] button:hover, .stButton > button:hover {
        background: #0B4F4A !important;
    }

    .disclaimer {
        margin-top: 30px;
        padding: 14px 18px;
        background: #FBF3E1;
        border: 1px solid #E9D5A0;
        border-radius: 10px;
        color: #6B5624;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="mediassist-header">
    <div class="icon">⚕️</div>
    <div>
        <h1>MediAssist AI</h1>
        <p>Document-grounded medical Q&A · Powered by Llama 3</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar: upload ----------
with st.sidebar:
    st.markdown("### 📄 Knowledge Base")
    st.caption("Upload a medical PDF to index it as the assistant's reference material.")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

    if uploaded_file and st.button("Upload & Index", use_container_width=True):
        with st.spinner("Indexing document..."):
            files = {"file": uploaded_file.getvalue()}
            try:
                res = requests.post(f"{API_URL}/upload", files=files, timeout=120)
                if res.ok:
                    st.success("Document indexed successfully.")
                else:
                    st.error(f"Upload failed: {res.status_code} {res.text}")
            except requests.exceptions.ConnectionError:
                st.error("Can't reach the backend. Is it running on port 8000?")

    st.markdown("---")
    st.caption("⚠️ Educational tool only - not a substitute for professional medical advice.")

# ---------- Chat ----------
st.markdown('<span class="section-label">Ask a Question</span>', unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

with st.form("ask_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "Question",
            placeholder="e.g. What are the symptoms of...",
            label_visibility="collapsed",
        )
    with col2:
        submitted = st.form_submit_button("Ask", use_container_width=True)

if submitted and query:
    with st.spinner("Consulting the reference document..."):
        try:
            res = requests.post(f"{API_URL}/ask", params={"query": query}, timeout=120)
            if res.ok:
                answer = res.json()["answer"]
                st.session_state.chat.append((query, answer))
            else:
                st.error(f"Request failed: {res.status_code} {res.text}")
        except requests.exceptions.ConnectionError:
            st.error("Can't reach the backend. Is it running on port 8000?")

for q, a in reversed(st.session_state.chat):
    st.markdown(f"""
    <div class="chat-row">
        <div class="bubble-user">
            <span class="bubble-label">You asked</span>{q}
        </div>
        <div class="bubble-ai">
            <span class="bubble-label">MediAssist</span>{a}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong> MediAssist AI answers only from the uploaded document
    and may not be complete or up to date. Always consult a qualified healthcare
    professional for diagnosis or treatment decisions.
</div>
""", unsafe_allow_html=True)