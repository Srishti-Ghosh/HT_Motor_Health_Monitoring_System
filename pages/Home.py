import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------ Page Config ------------------------
st.set_page_config(page_title="HT Motor Dashboard", layout="wide", page_icon="🏠")

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    if st.button("🔁 Go to Login"):
        st.switch_page("main.py")
    st.stop()

# Simulate logged-in user (replace with session-based logic)
user_name = st.session_state.get("user", "Guest")

st.markdown("""
    <style>
    /* Hide default navigation links */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Hide hamburger menu */
    [data-testid="collapsedControl"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# 🧑‍💼 SIDEBAR CONTENT
with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; padding-top: 0.5px; padding-bottom: 0.5px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/9131/9131529.png' width='70' style='border-radius:50%; margin-bottom: 0.5px;'/>
            <h4 style='margin: 0;'>Welcome,</h4>
            <h3 style='margin: 0; color: #1abc9c;'>{user_name}</h3>
        </div>
    """, unsafe_allow_html=True)
    # Navigation
    st.markdown("---")
    st.markdown("## Navigation")
    st.page_link("pages/Home.py", label="🏠 Diagnostics Dashboard")
    st.page_link("pages/RUL.py", label="📆 RUL & Health Estimation")
    st.page_link("pages/LEAP.py", label="🧪 LEAP Test Analyzer")
    st.page_link("pages/ENV.py", label="🏭 Environmental Damage Mapping")

    st.markdown("<div style='height: 90px;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # 🔓 Logout
    if st.button("🔓 Logout"):
        st.switch_page("pages/Logout.py")  
    
    st.markdown("""
        <div style='
            color: #bbbbbb;
            font-style: italic;
            font-size: 0.9rem;
        '>
        Made by Srishti Ghosh
        </div>
    """, unsafe_allow_html=True)

# ------------------------ Title ------------------------
st.title("🏠 HT Motor Diagnostics Dashboard")
st.markdown("""
    <style>
    .overview-section {
        margin-top: 2rem;
        color: white;
    }
    .overview-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1abc9c;
        margin-bottom: 0.5rem;
    }
    .overview-subtext {
        font-size: 1rem;
        color: #cccccc;
        margin-bottom: 2rem;
    }
    .overview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
        gap: 1.5rem;
    }
    .overview-card {
        background-color: #142f43;
        border-radius: 14px;
        padding: 1.2rem;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    .overview-card:hover {
        transform: translateY(-5px);
        background-color: #1e4563;
    }
    .overview-icon {
        font-size: 38px;
        margin-bottom: 0.6rem;
        color: #1abc9c;
    }
    .overview-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }
    .overview-description {
        font-size: 0.94rem;
        color: #dddddd;
    }
    .overview-highlight {
        background-color: #1abc9c22;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        color: #1abc9c;
        display: inline-block;
        font-size: 0.9rem;
        margin-top: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="overview-section">', unsafe_allow_html=True)

# Section Header
st.markdown("""
    <div class="overview-header">🔎 System Overview</div>
    <div class="overview-subtext">
        Monitor and maintain your HT motors using intelligent diagnostics. This dashboard provides <span style="color:#1abc9c;">real-time insights</span> into motor health, environment-induced degradation, and predictive maintenance schedules.
    </div>
""", unsafe_allow_html=True)

# Feature Cards
st.markdown('<div class="overview-grid">', unsafe_allow_html=True)

# -- RUL
st.markdown("""
    <div class="overview-card">
        <div class="overview-icon">📆</div>
        <div class="overview-title">RUL Estimation</div>
        <div class="overview-description">
            Calculates Remaining Useful Life using insulation metrics like IR, PI, DD, and Tan Delta by comparing against age and health thresholds.
            <div class="overview-highlight">AI-Based Health Index</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# -- LEAP
st.markdown("""
    <div class="overview-card">
        <div class="overview-icon">🧪</div>
        <div class="overview-title">LEAP Test Analyzer</div>
        <div class="overview-description">
            Interprets insulation diagnostics using industry-standard LEAP tests and flags abnormal patterns for damage type and location.
            <div class="overview-highlight">Insulation Health Checks</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# -- ENV
st.markdown("""
    <div class="overview-card">
        <div class="overview-icon">🏭</div>
        <div class="overview-title">Environmental Damage Mapping</div>
        <div class="overview-description">
            Uses test patterns and department data to detect environmental damage sources like <b>moisture</b>, <b>dust</b>, or <b>temperature stress</b>.
            <div class="overview-highlight">Department-Wise Impact</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close grid
st.markdown('</div>', unsafe_allow_html=True)  # close section
