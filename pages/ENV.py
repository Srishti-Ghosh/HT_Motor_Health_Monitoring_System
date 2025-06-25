# HT Motor Environmental Damage Analyzer with Improvements (Styled)

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import re

# ------------------------ Page Config ------------------------
st.set_page_config(page_title="HT Motor Diagnostics", page_icon="⚙️", layout="centered")

if not st.session_state.get("logged_in", False):
    st.error("Please login first.")
    if st.button("🔁 Go to Login"):
        st.switch_page("main")
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
    st.page_link("Home", label="🏠 Diagnostics Dashboard")
    st.page_link("RUL", label="📆 RUL & Health Estimation")
    st.page_link("LEAP", label="🧪 LEAP Test Analyzer")
    st.page_link("ENV", label="🏭 Environmental Damage Mapping")

    st.markdown("<div style='height: 90px;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # 🔓 Logout
    if st.button("🔓 Logout"):
        st.switch_page("Logout")  
    
    st.markdown("""
        <div style='
            color: #bbbbbb;
            font-style: italic;
            font-size: 0.9rem;
        '>
        Made by Srishti Ghosh
        </div>
    """, unsafe_allow_html=True)

# ------------------------ Title and Styling ------------------------

st.markdown("<h1 style='text-align:center; color:#4A90E2;'>⚙️ HT Motor Environmental Damage Analysis</h1>", unsafe_allow_html=True)
st.markdown("""
This interactive dashboard classifies and visualizes environmental damage to HT motors using LEAP+ test data.
The damage types considered are:
""")
            
st.markdown("""
<style>
/* Card container styling */
.dark-card {
    background-color: #1e1e1e;
    border-radius: 10px;
    padding: 18px 16px;
    text-align: left;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    transition: all 0.25s ease;
    border-left: 4px solid #3a3a3a;
    height: 150px;
}
.dark-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.4);
}

/* Icons */
.dark-icon {
    font-size: 22px;
    margin-bottom: 6px;
    color: #ffffffcc;
}

/* Title */
.dark-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: #ffffff;
}

/* Description */
.dark-desc {
    font-size: 13px;
    color: #bbbbbb;
    margin-top: 3px;
}

/* Accent border colors */
.moisture { border-color: #2d85d0; }
.dust     { border-color: #9b59b6; }
.temp     { border-color: #e74c3c; }
.normal   { border-color: #27ae60; }
</style>
""", unsafe_allow_html=True)

# Display 4 dark theme cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='dark-card moisture'>
        <div class='dark-icon'>💧</div>
        <div class='dark-title'>Moisture</div>
        <div class='dark-desc'>Water-induced insulation degradation</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='dark-card dust'>
        <div class='dark-icon'>🌫️</div>
        <div class='dark-title'>Dust</div>
        <div class='dark-desc'>Particulate buildup affecting cooling</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='dark-card temp'>
        <div class='dark-icon'>🌡️</div>
        <div class='dark-title'>Temperature</div>
        <div class='dark-desc'>Thermal overload or imbalance</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='dark-card normal'>
        <div class='dark-icon'>✅</div>
        <div class='dark-title'>Normal</div>
        <div class='dark-desc'>No abnormality detected</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.subheader("📤 Upload CSV File")
st.markdown("📌 Required columns: `Department`, `IR`, `PI`, `DD`, `TD_0.2`, `TD_1.0`, `TD_TipUp`, `Cap_TipUp`")

# ------------------------ File Upload ------------------------
uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = ['Department', 'IR', 'PI', 'DD', 'TD_0.2', 'TD_1.0', 'TD_TipUp', 'Cap_TipUp']
    if not all(col in df.columns for col in required_cols):
        st.error("❌ CSV must contain: " + ", ".join(required_cols))
    else:
        df['Department'] = df['Department'].astype(str).apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', x))
        features = ['IR', 'PI', 'DD', 'TD_TipUp', 'Cap_TipUp']

        # Reference patterns
        reference_patterns = {
            'Normal':       np.array([0.9, 0.9, 0.1, 0.1, 0.1]),
            'Moisture':     np.array([0.2, 0.2, 0.9, 0.8, 0.9]),
            'Dust':         np.array([0.5, 0.5, 0.8, 0.5, 0.8]),
            'Temperature':  np.array([0.6, 0.5, 0.5, 0.8, 0.6])
        }
        damage_types = list(reference_patterns.keys())
        ref_matrix = np.vstack(reference_patterns.values())
        ref_scaled = StandardScaler().fit_transform(ref_matrix)

        st.success(f"✅ Processing {len(df)} motors...")
        st.markdown("---")

        st.header("📊 Analysis Results")
        st.subheader("Environmental Damage Summary")
        # 🚀 Filter Controls — inside expander
        with st.expander("🔧 Filter Options", expanded=False):
            colf1, colf2 = st.columns([2, 1])
            filter_dept = colf1.multiselect("📌 Choose Departments", options=sorted(df['Department'].unique()), default=sorted(df['Department'].unique()))
            hide_normal = colf2.checkbox("🚫 Hide Normal Motors", value=False)

        # Filtering
        df_filtered = df[df['Department'].isin(filter_dept)]

        all_results = []

        for dept in df_filtered['Department'].unique():
            sub_df = df_filtered[df_filtered['Department'] == dept].dropna(subset=features)
            if len(sub_df) < 3:
                continue

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(sub_df[features])

            lowest_bic = np.inf
            best_n = 2
            for n in range(2, min(len(sub_df), 5)):
                gmm_try = GaussianMixture(n_components=n, random_state=42)
                gmm_try.fit(X_scaled)
                bic = gmm_try.bic(X_scaled)
                if bic < lowest_bic:
                    best_n = n
                    lowest_bic = bic

            gmm = GaussianMixture(n_components=best_n, random_state=42)
            clusters = gmm.fit_predict(X_scaled)
            sub_df = sub_df.copy()
            sub_df['Cluster'] = clusters

            cluster_means = sub_df.groupby('Cluster')[features].mean()
            cluster_scaled = StandardScaler().fit_transform(cluster_means)

            sim = cosine_similarity(cluster_scaled, ref_scaled)
            cluster_to_label = {i: damage_types[np.argmax(sim[i])] for i in range(sim.shape[0])}
            cluster_confidence = {i: np.max(sim[i]) for i in range(sim.shape[0])}

            sub_df['Predicted_Damage'] = sub_df['Cluster'].map(cluster_to_label)
            sub_df['Confidence'] = sub_df['Cluster'].map(cluster_confidence)
            sub_df['Department'] = dept

            all_results.append(sub_df)

        if all_results:
            final_df = pd.concat(all_results).reset_index(drop=True)

            if hide_normal:
                final_df = final_df[final_df['Predicted_Damage'] != 'Normal']

            damage_counts = final_df.groupby(['Department', 'Predicted_Damage']).size().unstack().fillna(0)
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            damage_counts.plot(kind='bar', stacked=True, ax=ax1, colormap='Set2')
            ax1.set_ylabel("Number of Motors")
            ax1.set_title("Total Damage Count by Department")
            ax1.set_xticklabels(damage_counts.index, rotation=45, ha='right')
            st.pyplot(fig1)

            col1, col2 = st.columns([4, 6])
            with col1:
                st.subheader("Damage Feature Patterns")
                mean_features = final_df.groupby('Predicted_Damage')[features].mean()
                fig3, ax3 = plt.subplots(figsize=(8, 4))
                sns.heatmap(mean_features, annot=True, cmap='coolwarm', ax=ax3)
                st.pyplot(fig3)

                csv = final_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results CSV", csv, "ht_motor_damage_results.csv", "text/csv")

            with col2:
                st.subheader("Final Motor-Level Classification")
                st.dataframe(final_df[['Department'] + features + ['Predicted_Damage', 'Confidence']])

        else:
            st.warning("⚠️ No departments had enough data to cluster.")
