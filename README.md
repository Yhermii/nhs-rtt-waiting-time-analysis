# 🏥 NHS England — Referral to Treatment (RTT) Waiting Time Analysis

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly&logoColor=white)
![Colab](https://img.shields.io/badge/Google%20Colab-Notebook-F9AB00?logo=googlecolab&logoColor=white)

> **End-to-end analysis of NHS England elective waiting time data (September 2021 – February 2026), covering 232 weeks of national RTT pathway data. Includes data cleaning, exploratory analysis, interactive visualisations, and a predictive machine learning model.**

---

## 📊 Key Findings

| Metric | Value |
|--------|-------|
| 📈 Peak Total Waiting List | **7.68 million patients** |
| 🎯 NHS 18-Week Target | **92%** |
| ❌ Actual Average % Within 18 Weeks | **59%** — never met throughout the period |
| ⚠️ Peak 2-Year+ Waiters | **25,519 patients** |
| 🤖 ML Model R² Score | **0.9991** |
| 📉 ML Model MAE | **~14,968 patients (0.2% error)** |

---

## 🖼️ Dashboard Preview

> Interactive 4-panel Plotly dashboard covering:
> - Total waiting list over time
> - % seen within 18 weeks vs 92% NHS target
> - Long waiters (52w+ and 104w+)
> - Actual vs predicted waiting list size

*See `dashboard/nhs_rtt_dashboard.html` — download and open in any browser.*

---

## 📁 Repository Structure

```
nhs-rtt-waiting-time-analysis/
│
├── README.md                          ← You are here
├── nhs_rtt_analysis.ipynb             ← Full analysis notebook (Google Colab)
├── NHS_RTT_Analysis_Report.docx       ← Detailed written insights report
│
├── dashboard/
│   └── nhs_rtt_dashboard.html         ← Interactive Plotly dashboard
│
└── assets/
    ├── chart1_waiting_list.png        ← Total waiting list over time
    ├── chart2_18w_target.png          ← % within 18 weeks vs target
    ├── chart3_long_waiters.png        ← Long waiter trends
    ├── chart5_stacked_area.png        ← Wait band breakdown
    ├── chart6_heatmap.png             ← Monthly heatmap
    └── dashboard_preview.png          ← Dashboard screenshot
```

---

## 🔍 Project Overview

### What is RTT?
The **Referral to Treatment (RTT)** pathway measures the time from a GP referral to the start of consultant-led treatment. Under the **NHS Constitution**, 92% of patients on incomplete pathways should wait no longer than **18 weeks**. This is one of the most closely monitored performance standards in the NHS.

### Why does this matter?
The analysis period (2021–2026) captures one of the most turbulent periods in NHS history:
- 🦠 The aftermath of **COVID-19**, which caused mass postponement of elective procedures
- 🏥 **NHS industrial action** in 2023–2024, disrupting elective activity
- 📈 Sustained **demand growth** outpacing capacity recovery
- 🏛️ Government-led **elective recovery plans** from 2022 onwards

---

## 🛠️ Technical Stack

| Tool | Purpose |
|------|---------|
| `pandas` | Data loading, cleaning, transformation |
| `matplotlib` & `seaborn` | Static visualisations |
| `plotly` | Interactive dashboard |
| `scikit-learn` | Linear Regression model, train/test split, evaluation |
| `Google Colab` | Development environment |

---

## 🧹 Data Cleaning Challenges

The raw NHS Excel file required significant preprocessing — a common challenge with publicly published NHS data:

- ✅ Skipped 13 rows of publication metadata and NHS headers
- ✅ Manually assigned column names to replace mangled multi-level headers
- ✅ Removed footnote rows and disclaimer text embedded within the data range
- ✅ Converted date columns to `datetime` and numeric columns using `pd.to_numeric` with error coercion
- ✅ Handled missing values before modelling

---

## 📈 Analysis Workflow

```
Raw NHS Excel File
        ↓
  Data Loading & Cleaning
        ↓
  Exploratory Data Analysis (EDA)
        ↓
  5 Visualisations (matplotlib / seaborn)
        ↓
  Feature Engineering
        ↓
  Linear Regression Model (scikit-learn)
        ↓
  Model Evaluation (R², MAE)
        ↓
  Interactive Dashboard (Plotly)
        ↓
  Written Insights Report (Word)
```

---

## 🤖 Machine Learning Model

**Model:** Linear Regression  
**Target variable:** `total_waiting_list`  
**Features:**

| Feature | Description |
|---------|-------------|
| `days_since_start` | Days elapsed since September 2021 (captures time trend) |
| `within_18w` | Patients waiting within 18 weeks |
| `over_104w` | Patients waiting 2+ years |
| `pct_within_18w` | % of patients seen within 18 weeks (strongest predictor) |

**Key insight:** `pct_within_18w` had by far the largest coefficient, confirming that the percentage seen on time is the single strongest predictor of overall waiting list pressure.

> ⚠️ **Note on R² = 0.9991:** The near-perfect score reflects the steady growth trajectory of the NHS waiting list — a trend that linear models fit well. The model would not capture sudden shocks (e.g. industrial action, policy changes). Time-series methods (ARIMA, Prophet) would be more appropriate for forecasting.

---

## 📂 Data Source

- **Source:** NHS England Waiting List Minimum Data Set (WLMDS)
- **URL:** [NHS England Statistics — RTT Waiting Times](https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/)
- **File:** `WLMDS-Summary-to-22-Feb-2026.xlsx`
- **Published:** 12th March 2026
- **Coverage:** Week ending 19 September 2021 → Week ending 22 February 2026
- **Basis:** Commissioner-level, national aggregate

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/Yhermii/nhs-rtt-waiting-time-analysis.git
   ```

2. Open `nhs_rtt_analysis.ipynb` in [Google Colab](https://colab.research.google.com) or Jupyter

3. Upload the NHS Excel file when prompted (or download directly from the NHS England link above)

4. Run all cells in order

5. Open `dashboard/nhs_rtt_dashboard.html` in your browser to view the interactive dashboard

---

## 📄 Written Report

A full written insights report (`NHS_RTT_Analysis_Report.docx`) is included, covering:
- Executive Summary
- Background & NHS Context
- Key Findings with clinical interpretation
- ML Model methodology and results
- Conclusions & Policy Recommendations

---

## 👤 Author

**Adeyemi Abodunrin**  
Data Scientist | Healthcare Professional | Health Data Science

- 💼 [LinkedIn](https://www.linkedin.com/in/adeyemi-ao/)
- 🐙 [GitHub](https://github.com/Yhermii)

---

## 📜 Licence

This project is for portfolio and educational purposes. NHS data is used under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

---

*If you found this useful, please ⭐ the repository!*
