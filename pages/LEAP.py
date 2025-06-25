import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import numpy as np

# ----------- Diagnostic Logic -----------
def classify_insulation_health(ir, pi, dd, td_20, td_100, cap_tipup):
    td_tipup = td_100 - td_20

    def lvl(val, low, high): return 'Good' if val < low else 'Moderate' if val < high else 'Poor'

    IR = 'Good' if ir >= 0.1 else 'Moderate' if ir >= 0.05 else 'Poor'
    PI = 'Good' if pi >= 2 else 'Moderate' if pi >= 1.5 else 'Poor'
    DD = lvl(dd, 4, 10)
    TD20 = 'Low' if td_20 < 0.01 else 'High'
    TD100 = 'Low' if td_100 < 0.02 else 'High'
    TDt = lvl(abs(td_tipup), 0.8, 2.0)
    CT = lvl(cap_tipup, 0.005, 0.015)

    # Diagnosis Rules
    if all(x == 'Good' for x in [IR, PI, DD, TDt, CT]):
        diagnosis = "Healthy insulation"
        action = "No action"
        location = "-"
    elif IR == 'Poor' and PI == 'Poor' and DD == 'Poor':
        diagnosis = "Surface moisture and trapped aging"
        action = "Clean & dry, retest"
        location = "Stator surface / terminal box"
    elif TDt == 'Poor' and CT == 'Poor':
        diagnosis = "Voids + stress zones emerging"
        action = "Schedule partial reinsulation"
        location = "Interlayer insulation"
    elif TDt == 'Poor' and CT == 'Moderate':
        diagnosis = "Early partial discharge risk"
        action = "Monitor monthly"
        location = "End winding, stress zones"
    elif TD20 == 'High' and TD100 == 'High' and CT == 'Good':
        diagnosis = "Uniform dielectric loss (contamination)"
        action = "Clean & dry"
        location = "Surface insulation"
    elif TDt == 'Poor' and CT == 'Good':
        diagnosis = "Voltage-sensitive dielectric aging"
        action = "Monitor trending"
        location = "Bulk insulation"
    elif CT == 'Poor' and TDt == 'Good':
        diagnosis = "Delamination or geometry deformation"
        action = "Inspect physical winding structure"
        location = "Slot insulation"
    elif DD == 'Poor' and TDt != 'Poor':
        diagnosis = "Embedded moisture"
        action = "Dry motor internally and retest"
        location = "Bulk winding insulation"
    elif IR == 'Poor' and DD == 'Good':
        diagnosis = "Surface leakage"
        action = "Drying & visual inspection"
        location = "Motor body / cable box"
    elif IR == 'Moderate' and PI == 'Moderate' and DD == 'Moderate':
        diagnosis = "Aging trend beginning"
        action = "Retest in 3 months"
        location = "General insulation"
    elif PI == 'Moderate' and TD100 == 'High':
        diagnosis = "Minor dielectric stress"
        action = "Trend analysis & monitoring"
        location = "End winding"
    elif TDt == 'Moderate' and CT == 'Good':
        diagnosis = "Early voltage tracking"
        action = "Flag for monitoring"
        location = "Corona-prone zones"
    elif TD20 == 'High' and CT == 'Poor':
        diagnosis = "Capacitance shift with aging"
        action = "Plan full inspection"
        location = "Winding insulation"
    elif IR == 'Moderate' and TDt == 'Poor' and CT == 'Poor':
        diagnosis = "Developing delamination under stress"
        action = "Offline LEAP+ recommended"
        location = "Slot region / taping"
    elif PI == 'Poor' and TD100 == 'High':
        diagnosis = "Insulation wear with increased loss"
        action = "Drying + trending"
        location = "Mid-slot insulation"
    else:
        diagnosis = "Unclassified"
        action = "Full diagnostics required"
        location = "To be inspected"

    # Confidence Score
    weights = {'IR': 1, 'PI': 1, 'DD': 1, 'TDt': 3, 'CT': 2}
    status_map = {'Good': 2, 'Moderate': 1, 'Poor': 0}
    statuses = {'IR': IR, 'PI': PI, 'DD': DD, 'TDt': TDt, 'CT': CT}
    score = sum(weights[t] * status_map[statuses[t]] for t in statuses)
    max_score = sum(w * 2 for w in weights.values())
    confidence = int(score / max_score * 100)

    return {
        "Diagnosis": diagnosis,
        "Action": action,
        "Location": location,
        "Confidence (%)": confidence,
        "Statuses": statuses
    }

# ----------- Streamlit UI -----------
st.set_page_config("HT Motor LEAP Analyzer", layout="wide", page_icon="⚙️")

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

st.markdown("<h1 style='text-align:center; color:#4A90E2;'>⚙️ HT Motor Insulation Health Diagnostics</h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔹 Single Motor Entry", "📤 Bulk Upload & Analysis"])

# ---------- SINGLE ENTRY ----------
with tab1:
    st.subheader("🔍 Enter Single Motor Test Values")

    with st.form("test_values", clear_on_submit=False):
        cols = st.columns(3)
        with cols[0]:
            ir = st.number_input("Insulation Resistance (GΩ)", value=1.0)
            pi = st.number_input("Polarization Index", value=2.0)
        with cols[1]:
            dd = st.number_input("Dielectric Discharge (μA)", value=1.0)
            td20 = st.number_input("Tan Δ @20% U₀", value=0.004, format="%.4f")
        with cols[2]:
            td100 = st.number_input("Tan Δ @100% U₀", value=0.004, format="%.4f")
            cap_tipup = st.number_input("Cap Tip-Up", value=0.005, format="%.4f")
        run = st.form_submit_button("Run Diagnosis")

    if run:
        res = classify_insulation_health(ir, pi, dd, td20, td100, cap_tipup)
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        status = res["Statuses"]
        confidence = res["Confidence (%)"]
        color = 'green' if confidence >= 80 else 'orange' if confidence >= 50 else 'red'

        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Confidence Score", f"{confidence}%")
            st.markdown(
                f"<div style='font-size:0.9rem; color:gray;'>Confidence Score reflects severity-weighted degradation from test values. ", unsafe_allow_html=True)
        with col2:
            st.markdown("#### 🧬 Diagnosis Summary")
            st.success(f"**Diagnosis:** {res['Diagnosis']}")
            st.info(f"**Action:** {res['Action']} • **Location:** {res['Location']}")

        st.markdown("#### 🕸️ Radar Chart of Test Conditions")
        level_map = {"Poor": 0, "Moderate": 1, "Good": 2}
        radar_keys = ['IR', 'PI', 'DD', 'TDt', 'CT']
        radar_vals = [level_map[status[k]] for k in radar_keys]
        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(
            r=radar_vals,
            theta=['IR', 'PI', 'DD', 'TD TipUp', 'Cap TipUp'],
            fill='toself',
            name="Health Levels",
            line=dict(color=color)
        ))
        radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 2], tickvals=[0, 1, 2],
                                       ticktext=["Poor", "Moderate", "Good"])),
            showlegend=False
        )
        st.plotly_chart(radar, use_container_width=True)

# ---------- BULK UPLOAD ----------
with tab2:
    st.subheader("📤 Upload CSV File")
    st.markdown("📌 Required columns: `IR`, `PI`, `DD`, `TanDelta_20`, `TanDelta_100`, `Cap_TipUp`")
    
    file = st.file_uploader("Upload CSV", type="csv")
    if file:
        df = pd.read_csv(file)

        # Strip and standardize column names
        df.columns = [c.strip().replace(" ", "_") for c in df.columns]

        # Handle duplicate columns safely
        if df.columns.duplicated().any():
            dup_cols = df.columns[df.columns.duplicated()].tolist()
            st.warning(f"⚠️ Duplicate columns found and renamed: {dup_cols}")
            df.columns = pd.io.parsers.ParserBase({'names': df.columns})._maybe_dedup_names(df.columns)

        required = ['IR', 'PI', 'DD', 'TanDelta_20', 'TanDelta_100', 'Cap_TipUp']
        if not all(col in df.columns for col in required):
            missing = [col for col in required if col not in df.columns]
            st.error(f"❌ Missing required columns: {missing}")
        else:
            results = []
            for _, row in df.iterrows():
                r = classify_insulation_health(
                    row['IR'], row['PI'], row['DD'],
                    row['TanDelta_20'], row['TanDelta_100'],
                    row['Cap_TipUp']
                )
                r_flat = {
                    "Diagnosis": r["Diagnosis"],
                    "Action": r["Action"],
                    "Location": r["Location"],
                    "Confidence (%)": r["Confidence (%)"],
                    **r["Statuses"]
                }
                results.append(r_flat)

            results_df = pd.DataFrame(results)

            # Ensure no duplicate columns when concatenating
            cols_to_avoid = set(df.columns)
            results_df.columns = [
                col if col not in cols_to_avoid else f"{col}_classified" for col in results_df.columns
            ]

            output_df = pd.concat([df.reset_index(drop=True), results_df.reset_index(drop=True)], axis=1)

            st.success(f"✅ Processed {len(output_df)} motors.")
            st.markdown("---")

            st.header("🧰 Insulation Diagnosis with Degradation Location / Action Plan")
            st.dataframe(output_df)

            st.header("📊 Visual Overview")
            cols = st.columns(2)
            with cols[0]:
                st.subheader("Diagnosis Distribution")

                if "Diagnosis" in output_df.columns:
                    diagnosis_counts = output_df["Diagnosis"].value_counts()
                    total = diagnosis_counts.sum()
                    percentages = (diagnosis_counts / total * 100).round(1)

                    colors = sns.color_palette("Set2", len(diagnosis_counts))
                    fig = plt.figure(figsize=(7, 5), constrained_layout=True)
                    ax = fig.add_subplot()

                    wedges, texts = ax.pie(
                        diagnosis_counts,
                        labels=None,
                        colors=colors,
                        startangle=140,
                        wedgeprops=dict(width=0.4, edgecolor='w'),
                        autopct=None
                    )

                    for i, p in enumerate(wedges):
                        ang = (p.theta2 - p.theta1)/2. + p.theta1
                        y = np.sin(np.deg2rad(ang))
                        x = np.cos(np.deg2rad(ang))
                        ha = {-1: "right", 1: "left"}[int(np.sign(x))]
                        connectionstyle = f"angle,angleA=0,angleB={ang}"
                        ax.annotate(f"{percentages[i]}%",
                                    xy=(x, y),
                                    xytext=(1.2*np.sign(x), 1.2*y),
                                    horizontalalignment=ha,
                                    fontsize=11,
                                    bbox=dict(boxstyle="round,pad=0.2", fc="white", edgecolor="none"),
                                    arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle, color=colors[i]))

                    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
                    fig.gca().add_artist(centre_circle)
                    ax.axis("equal")

                    ax.legend(wedges, diagnosis_counts.index, title="Diagnosis", loc="center left", bbox_to_anchor=(1, 0.5))
                    ax.set_title("Motor Health Diagnosis Summary", fontsize=14, weight='bold')
                    st.pyplot(fig)

            with cols[1]:
                st.subheader("Health Classification")

                leap_tests = ['IR_classified', 'PI_classified', 'DD_classified', 'TDt', 'CT']
                leap_tests = [col for col in leap_tests if col in output_df.columns and output_df[col].dtype == 'object']

                if leap_tests:
                    summary_all = pd.DataFrame({
                        'Good': (output_df[leap_tests] == 'Good').sum(),
                        'Moderate': (output_df[leap_tests] == 'Moderate').sum(),
                        'Poor': (output_df[leap_tests] == 'Poor').sum()
                    })

                    fig_all = plt.figure(figsize=(7, 5), constrained_layout=True)
                    ax_all = fig_all.add_subplot()
                    summary_all.plot(kind='bar', stacked=True, ax=ax_all, color=['green', 'orange', 'red'])

                    ax_all.set_title("Health Classification by LEAP Test")
                    ax_all.set_xlabel("LEAP Test")
                    ax_all.set_ylabel("Count")
                    ax_all.legend(title="Condition", bbox_to_anchor=(1.05, 1), loc='upper left')
                    plt.xticks(rotation=45)
                    st.pyplot(fig_all)


            st.download_button("⬇️ Download Results CSV", data=output_df.to_csv(index=False).encode(),
                               file_name="diagnostic_results.csv", mime="text/csv")

