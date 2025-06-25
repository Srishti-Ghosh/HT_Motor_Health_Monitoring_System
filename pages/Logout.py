import streamlit as st
import time

# --- Hide Sidebar ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        .logout-box {
            margin-top: 6rem;
            text-align: center;
            color: white;
        }
        .logout-title {
            font-size: 2rem;
            font-weight: bold;
            color: #1abc9c;
        }
        .logout-sub {
            font-size: 1rem;
            color: #cccccc;
            margin-top: 1rem;
        }
        .countdown {
            font-size: 2.5rem;
            font-weight: bold;
            margin-top: 2rem;
            color: #ff6b6b;
            animation: pulse 1s ease-in-out infinite;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# --- Clear session ---
st.session_state.clear()

# --- Main Display ---
st.markdown("""
    <div class="logout-box">
        <div class="logout-title">🔒 You’ve been logged out</div>
        <div class="logout-sub">Redirecting to login page in <span style='color:#1abc9c;'>a moment</span>...</div>
    </div>
""", unsafe_allow_html=True)

# --- Countdown animation ---
countdown_placeholder = st.empty()

for i in range(3, 0, -1):
    countdown_placeholder.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
    time.sleep(1)

# --- Redirect to login page (main.py) ---
st.switch_page("main")
