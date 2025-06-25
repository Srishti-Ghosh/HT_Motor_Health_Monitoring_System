import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np
import plotly.express as px

# Scoring functions
def score_ir(val): return 10 if val >= 1 else 8 if val >= 0.1 else 6 if val >= 0.05 else 2
def score_pi(val): return 10 if val >= 2 else 8 if val >= 1.5 else 6 if val >= 1 else 2
def score_dd(val): return 10 if val <= 1 else 8 if val <= 4 else 6 if val <= 10 else 2
def score_tdtu(val): return 10 if val < abs(0.8) else 8 if val < abs(1.0) else 6 if val < abs(2.0) else 2
def score_captip(val): return 10 if val < 5 else 8 if val < 10 else 6 if val < 15 else 2

# Page setup
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

st.markdown("""
<style>
.metric-style div {
    background-color: #1e1e1e;
    padding: 1.2rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    border: 1px solid #dce0e6;
    color: #1e1e1e !important;
}
.metric-style span {
    font-size: 1.4rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:#4A90E2;'>⚙️ HT Motor Health & RUL Estimator</h1>", unsafe_allow_html=True)

# Tabs for switching
tab1, tab2 = st.tabs(["🔹 Single Motor Entry", "📤 Bulk Upload & Analysis"])

# -------------------- SINGLE INPUT TAB -------------------- #
with tab1:
    with st.form("motor_form"):
        st.subheader("🔍 Enter Test Values")
        col1, col2 = st.columns(2)
        with col1:
            ir = st.number_input("🧪 IR (GΩ)", 0.0, 100.0, 1.0)
            dd = st.number_input("⚡ DD (mA)", 0.0, 100.0, 5.0)
            test_year = st.number_input("🗓️ Test Year", 1990, 2030, 2024)
            cap_tip = st.slider("📏 Cap Tip-Up (pF)", 0.0, 100.0, 10.0)
        with col2:
            pi = st.number_input("🔁 PI", 0.0, 10.0, 1.5)
            td_tu = st.number_input("🌀 Tan Delta Tip-Up", 0.0, 10.0, 1.5)
            mfg_year = st.number_input("🏭 Manufacturing Year", 1970, 2024, 2000)
            av_age = st.slider("❤️ Average Motor Life", 0.0, 100.0, 30.0)

        submit = st.form_submit_button("🔎 Estimate Health")

    if submit:
        if test_year < mfg_year:
            st.error("❌ Test year can't be before manufacturing year.")
        else:
            age = test_year - mfg_year
            s_ir = score_ir(ir)
            s_pi = score_pi(pi)
            s_dd = score_dd(dd)
            s_td = score_tdtu(td_tu)
            s_cap = score_captip(cap_tip)

            hi = (s_ir + s_pi + s_dd + s_td * 2 + s_cap * 2) / 7
            rul = (hi / 10) * (av_age - age)

            if hi >= 8:
                condition = "🟢 Excellent"
            elif hi >= 6:
                condition = "🟡 Good"
            elif hi >= 4:
                condition = "🟠 Moderate"
            else:
                condition = "🔴 Critical"

            st.markdown('<div class="metric-style">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Health Index", f"{hi:.2f}/10")
            with col2:
                st.metric("Est. RUL", f"{rul:.2f} yrs")
            with col3:
                st.metric("Condition", condition)

            st.markdown('</div>', unsafe_allow_html=True)

            # Score breakdown
            scores = {
                "IR": s_ir, "PI": s_pi, "DD": s_dd,
                "Tan Delta Tip-Up": s_td, "Cap Tip-Up": s_cap
            }

            st.subheader("📊 Score Breakdown")
            st.bar_chart(pd.DataFrame.from_dict(scores, orient='index', columns=["Score"]))

            # Side-by-side layout for radar and gauge charts
            radar_col, gauge_col = st.columns(2)

            with radar_col:
                st.markdown("**🕸️ Score Distribution (Radar)**")
                radar = go.Figure()
                radar.add_trace(go.Scatterpolar(
                    r=list(scores.values()),
                    theta=list(scores.keys()),
                    fill='toself',
                    line=dict(color='royalblue')
                ))
                radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
                st.plotly_chart(radar, use_container_width=True)

            with gauge_col:
                st.markdown("**🧠 Health Index Gauge**")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=hi,
                    title={'text': "Health Index"},
                    gauge={
                        'axis': {'range': [0, 10]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 4], 'color': "red"},
                            {'range': [4, 6], 'color': "orange"},
                            {'range': [6, 8], 'color': "yellow"},
                            {'range': [8, 10], 'color': "green"},
                        ]
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
                

# -------------------- BULK UPLOAD TAB -------------------- #
with tab2:
    st.subheader("📥 Upload CSV with LEAP+ Test Data")
    st.markdown("📌 Required columns: `IR`, `PI`, `DD`, `TanDelta_20`, `TanDelta_100`, `Cap_TipUp`, `Test_Year`, `Manufacturing_Year`")
    uploaded = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        df.columns = [c.strip().replace(" ", "_") for c in df.columns]

        required = ['IR', 'PI', 'DD', 'TanDelta_20', 'TanDelta_100', 'Cap_TipUp', 'Test_Year', 'Manufacturing_Year']
        if not all(col in df.columns for col in required):
            st.error("❌ Missing required columns: " + ", ".join(required))
        else:
            df["TanDelta_TipUp"] = df["TanDelta_100"] - df["TanDelta_20"]
            df["Age"] = df["Test_Year"] - df["Manufacturing_Year"]
            df['Score_IR'] = df['IR'].apply(score_ir)
            df['Score_PI'] = df['PI'].apply(score_pi)
            df['Score_DD'] = df['DD'].apply(score_dd)
            df['Score_TD_TU'] = df['TanDelta_TipUp'].apply(score_tdtu)
            df['Score_Cap_TU'] = df['Cap_TipUp'].apply(score_captip)

            df['Health_Index'] = (
                df['Score_IR'] + df['Score_PI'] + df['Score_DD'] +
                df['Score_TD_TU'] * 2 + df['Score_Cap_TU'] * 2
            ) / 7

            df['Estimated_RUL'] = (df['Health_Index'] / 10) * (100 - df['Age'])

            def label(hi):
                if hi >= 8: return "Excellent"
                elif hi >= 6: return "Good"
                elif hi >= 4: return "Moderate"
                else: return "Critical"
            df['Condition'] = df['Health_Index'].apply(label)

            st.success(f"✅ Processed {len(df)} motors.")
            st.markdown("---")
            st.header("💊 HT Motor Health and Remaining Useful Life")
            st.dataframe(df[['IR', 'PI', 'DD', 'TanDelta_TipUp', 'Cap_TipUp', 'Age', 'Health_Index', 'Estimated_RUL', 'Condition']])

            # Charts
            st.subheader("📊 Visual Overview")

            # Prepare histogram-like data
            hi_counts = df['Health_Index'].round(1).value_counts().sort_index()
            hi_df = pd.DataFrame({'Health_Index': hi_counts.index, 'Count': hi_counts.values})

            # 📊 Health Index Distribution
            st.markdown("#### Health Index")

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=hi_df, x='Health_Index', y='Count', palette='viridis', ax=ax)
            ax.set_xlabel('Health Index (rounded)')
            ax.set_ylabel('Motor Count')
            sns.despine()
            st.pyplot(fig)

            # 📊 Pie and Scatter in Columns
            col1, col2 = st.columns([4.6,5.4])

            with col1:
                st.markdown("#### Condition Breakdown")
                condition_counts = df['Condition'].value_counts()
                labels = condition_counts.index
                sizes = condition_counts.values
                colors = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]  # Match original color scheme

                fig, ax = plt.subplots(figsize=(5, 5))
                wedges, texts, autotexts = ax.pie(
                    sizes,
                    labels=labels,
                    colors=colors,
                    autopct='%1.1f%%',
                    startangle=140,
                    pctdistance=0.85,
                    wedgeprops=dict(width=0.4)
                )

                # Add center circle for donut style
                centre_circle = plt.Circle((0, 0), 0.60, fc='white')
                ax.add_artist(centre_circle)
                ax.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left')
                ax.axis('equal')
                st.pyplot(fig)

            with col2:
                st.markdown("#### RUL vs Age")
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.scatterplot(
                    data=df,
                    x='Age',
                    y='Estimated_RUL',
                    hue='Condition',
                    palette={
                        "Excellent": "#2ecc71",
                        "Good": "#f1c40f",
                        "Moderate": "#e67e22",
                        "Critical": "#e74c3c"
                    },
                    s=60,
                    edgecolor='black',
                    ax=ax
                )
                ax.set_xlabel('Motor Age (yrs)')
                ax.set_ylabel('RUL (yrs)')
                ax.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left')
                sns.despine()
                plt.tight_layout()
                st.pyplot(fig)

            # Heatmap
            st.subheader("🌡️ Health Score Heatmap")
            try:
                fig, ax = plt.subplots(figsize=(10, min(0.4 * len(df), 12)))
                heat_data = df[['Score_IR', 'Score_PI', 'Score_DD', 'Score_TD_TU', 'Score_Cap_TU']]
                sns.heatmap(heat_data, cmap="RdYlGn", annot=True, cbar=True, ax=ax)
                st.pyplot(fig)
            except:
                st.warning("⚠️ Heatmap could not be rendered.")

            # Download button
            st.download_button("⬇️ Download Processed Data", data=df.to_csv(index=False).encode(),
                               file_name="motor_health_results.csv", mime="text/csv")
