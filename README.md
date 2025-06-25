# ⚙️ HT Motor Health Monitoring System – Streamlit App

A comprehensive AI-driven web application built with **Streamlit** to monitor, diagnose, and analyze **HT Motor insulation health**, **environmental damage**, and **predict remaining useful life (RUL)** using **LEAP+ test data** and unsupervised clustering.

[🔗 See Live Demo](https://ht-motor-health-monitoring-system.streamlit.app/)

---

## 🌟 Features

🔹 **Login Authentication**

🔹 **Single & Bulk Diagnostics using LEAP+ tests**

🔹 **Confidence-based health scoring and radar visualization**

🔹 **Environmental damage classification (moisture, dust, thermal)**

🔹 **Motor-level clustering and department-level summary**

🔹 **Interactive plots: Pie, Bar, Heatmaps, Radar**

🔹 **Session-aware Logout & Page Navigation**

---

## 🧩 App Structure

```plaintext
📁 pages/
│   ├── Home.py           # Diagnostics dashboard and motor health metrics
│   ├── RUL.py            # RUL & health index prediction 
│   ├── LEAP.py           # LEAP+ test analyzer: health classification and diagnostics
│   ├── ENV.py            # Environmental damage mapping via clustering
│   └── Logout.py         # Logout page with animated redirect
├── main.py               # Login page
├── requirements.txt      # Dependencies 
└── README.md             # You are here
```

---

## 🔐 Authentication

Only logged-in users can access the dashboard pages. Users must:

* Enter correct credentials on `main.py`
* After logout via the sidebar, users are redirected with a countdown animation

---

## 📆 Health and RUL Estimation

Found in: `pages/RUL.py`

### 🔍 Purpose:

This module estimates the **Remaining Useful Life (RUL)** and **health score** of HT motors using historical **LEAP+ test data**, age, and degradation factors.

### 📥 Required Input:

Upload a CSV file containing:

```csv
IR, PI, DD, TanDelta_20, TanDelta_100, Cap_TipUp, Manufacturing_Year, Test_Year
```

### 📊 Output Metrics:

* **Health Index (%)**: Computed from test performance, age, and severity
* **RUL (Years)**: Predicted remaining service life based on test degradation trends
* **Environmental Damage Factor**: Integrated if ENV module data is merged
* **Next Servicing Date**: Auto-calculated based on current trends and health decline

### 🧠 Model Features:

* Rule-based scoring of insulation parameters
* Incorporates **age-based degradation**
* Visualizes:

  * Health distribution (bar chart)
  * Group scatter plot of conditions vs RUL
* Integrates with bulk motor fleet data for monitoring across departments

---

## 🔬 LEAP+ Insulation Health Analyzer

Found in: `pages/LEAP.py`

### ✅ Inputs:

* **IR** (Insulation Resistance)
* **PI** (Polarization Index)
* **DD** (Dielectric Discharge)
* **Tan Delta** at 20% and 100% voltage
* **Capacitance Tip-Up**

### 🧠 Features:

* Rule-based insulation diagnosis with 90%+ scenarios
* Classifies insulation status as Good / Moderate / Poor
* Suggests corrective actions and problem locations
* Computes **Confidence Score**
* Radar chart shows status distribution

### 📂 Bulk Mode:

Upload a CSV with columns:

```csv
IR, PI, DD, TanDelta_20, TanDelta_100, Cap_TipUp
```

Get diagnosis, action plan, radar data, and download full results.

---

## 🏭 Environmental Damage Analyzer

Found in: `pages/ENV.py`

### 📁 Required Input Format:

```csv
Department, IR, PI, DD, TD_0.2, TD_1.0, TD_TipUp, Cap_TipUp
```

### 🔍 Functionality:

* Uses **Gaussian Mixture Models** for unsupervised clustering
* Compares clusters to known reference patterns using **cosine similarity**
* Labels clusters as:

  * Moisture Damage 💧
  * Dust Contamination 🌫️
  * Temperature Overload 🌡️
  * Normal ✅

### 📊 Outputs:

* Stacked bar plots of damage type per department
* Confidence scores for predicted labels
* Feature heatmaps by damage type
* Filter to exclude normal motors

---

## 🔁 Logout

Found in: `pages/Logout.py`

* Clears session state
* Shows styled message and countdown
* Redirects automatically to login (`main.py`)

---

## 🖼️ Visual Elements

* Custom sidebar with navigation
* Emoji-labeled tabs and buttons
* Dark-themed feature cards
* Plotly Radar Chart
* Seaborn heatmaps & bar plots
* Matplotlib-based donut charts

---

## 🚀 Getting Started

### 🧰 Prerequisites

Make sure you have Python 3.8+ and install Streamlit and dependencies:

```bash
pip install streamlit pandas numpy seaborn matplotlib scikit-learn plotly
```

---

### ▶️ Run the App

```bash
streamlit run main.py
```

---

## 👤 Developer

Made with 💡 by **Srishti Ghosh**

---
