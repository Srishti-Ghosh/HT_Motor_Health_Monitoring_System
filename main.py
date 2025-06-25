import streamlit as st
import hashlib
from PIL import Image

# ✅ SET PAGE CONFIG FIRST
st.set_page_config(page_title="HT Motor Login", page_icon="🔐", layout="centered")

# ✅ Hide sidebar (after page config)
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
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

# ✅ Initialize session state
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Tata_logo.svg/1200px-Tata_logo.svg.png"
users = {
    "admin": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4",  # 1234
    "engineer": "88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589"  # abcd
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.switch_page("pages/Home.py")

# Render login UI
st.markdown(f"""
    <div style="text-align: center;">
        <img src="{LOGO_URL}" width="120" />
        <h2 style="margin-top: 1rem; color: #0765ff;">HT Motor Diagnostics Login</h2>
        <p style="color: gray;">Enter your credentials to continue</p>
    </div>
""", unsafe_allow_html=True)

with st.container():
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            if users.get(username) == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.switch_page("pages/Home.py")
            else:
                st.error("❌ Invalid username or password.")
