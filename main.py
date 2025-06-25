import streamlit as st
import hashlib
from PIL import Image
import time

# ✅ SET PAGE CONFIG FIRST
st.set_page_config(page_title="HT Motor Diagnostics", page_icon="⚙️", layout="centered")

# ✅ Hide sidebar (after page config)
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        .fade-in {
            animation: fadeIn 1.5s ease-in;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .login-card {
            background-color: #f5f7fa;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ THEN initialize session state and other logic
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Tata_logo.svg/1200px-Tata_logo.svg.png"
users = {
    "admin": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", #1234
    "engineer": "88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589" #abcd
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.switch_page("pages/Home.py")

# Render login UI
st.markdown(f"""
    <div class="fade-in" style="text-align: center;">
        <img src="{LOGO_URL}" width="120" />
        <h2 style="margin-top: 1rem; color: #0765ff;">HT Motor Diagnostics Login</h2>
        <p style="color: gray;">Enter your credentials to continue</p>
    </div>
""", unsafe_allow_html=True)

with st.container():
    with st.form("login_form"):
        st.markdown("""
        <style>
            .block-container > div:first-child > div > div:first-child > div:nth-child(1) {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)

        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        login = st.form_submit_button("Login")

        st.markdown('</div>', unsafe_allow_html=True)

        if login:
            if users.get(username) == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("✅ Login successful! Redirecting...")
                time.sleep(2)  # Pause for 2 second
                st.switch_page("pages/Home.py")

            else:
                st.error("❌ Invalid username or password.")




