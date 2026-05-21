import streamlit as st
import pandas as pd
import joblib
from auth import show_auth_page
from dashboard import save_prediction, show_dashboard

if "user" not in st.session_state:
    show_auth_page()
    st.stop()

st.set_page_config(page_title="LoanSense AI", page_icon="🏦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&family=Geist:wght@300;400;500;600&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
}

html, body, [class*="css"], .stApp {
    font-family: 'Geist', sans-serif !important;
    background-color: #0c0f1a !important;
    color: #eef0f8 !important;
}

.stApp {
    background: #0c0f1a !important;
}

header[data-testid="stHeader"] {
    display: none !important;
}

section.main > div {
    max-width: 720px !important;
    margin: 0 auto !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

.block-container {
    max-width: 720px !important;
    margin: 0 auto !important;
    padding-top: 0 !important;
}

/* ───────── NAVBAR ───────── */

.nav-wrapper {
    width: 100%;
    background: #080b14;
    border-bottom: 1px solid #161c30;
    padding: 10px 22px;
    margin: -1rem -1rem 0 -1rem;
}

.nav-left {
    display: flex;
    align-items: center;
    gap: 10px;
    overflow: hidden;
}

.nav-logo {
    font-family: 'Fraunces', serif;
    font-size: 1.2rem;
    color: #eef0f8;
    font-weight: 600;
    letter-spacing: -0.5px;
    white-space: nowrap;
}

.nav-logo em {
    font-style: italic;
    color: #6c8fff;
}

.nav-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #6c8fff;
    opacity: 0.7;
    flex-shrink: 0;
}

.nav-email {
    font-size: 0.72rem;
    color: #4a5580;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

div[data-testid="column"]:nth-of-type(2) .stButton > button,
div[data-testid="column"]:nth-of-type(3) .stButton > button {

    background: transparent !important;
    color: #4a5580 !important;

    border: 1px solid #1e2540 !important;
    border-radius: 8px !important;

    padding: 8px 16px !important;

    font-size: 0.7rem !important;
    font-weight: 600 !important;

    letter-spacing: 1px !important;
    text-transform: uppercase !important;

    min-width: 110px !important;
    width: 100% !important;

    height: 42px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    white-space: nowrap !important;

    transition: all 0.15s ease !important;
}

div[data-testid="column"]:nth-of-type(2) .stButton > button:hover {
    color: #eef0f8 !important;
    border-color: #6c8fff !important;
    background: #0f1528 !important;
}

div[data-testid="column"]:nth-of-type(3) .stButton > button:hover {
    color: #f87171 !important;
    border-color: #4a1515 !important;
    background: #150a0a !important;
}

/* ───────── HERO ───────── */

.hero {
    background: linear-gradient(180deg, #0f1528 0%, #0c0f1a 100%);
    padding: 26px 4px 20px;
    border-bottom: 1px solid #161c30;
    margin-bottom: 20px;
}

.hero-eyebrow {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #6c8fff;
    margin-bottom: 8px;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 1.75rem;
    color: #eef0f8;
    font-weight: 300;
    line-height: 1.2;
    margin-bottom: 6px;
}

.hero-title strong {
    font-weight: 600;
}

.hero-sub {
    font-size: 0.8rem;
    color: #4a5580;
    font-weight: 400;
    line-height: 1.5;
}

/* ───────── SECTIONS ───────── */

.section {
    background: #0f1528;
    border: 1px solid #1e2540;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
}

.section-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #4a5580;
    margin-bottom: 16px;
}

/* ───────── INPUTS ───────── */

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    color: #4a5580 !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: #080b14 !important;
    border: 1px solid #1e2540 !important;
    border-radius: 8px !important;
    color: #c8cfe8 !important;
    font-size: 0.875rem !important;
}

div[data-testid="stNumberInput"] input {
    background: #080b14 !important;
    border: 1px solid #1e2540 !important;
    border-radius: 8px !important;
    color: #eef0f8 !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
}

/* ───────── BUTTON ───────── */

.predict-btn div.stButton > button {
    width: 100% !important;
    background: #6c8fff !important;
    color: #080b14 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

.predict-btn div.stButton > button:hover {
    opacity: 0.85 !important;
}

/* ───────── RESULT ───────── */

.result-approved {
    background: #060f10;
    border: 1px solid #0d4429;
    border-radius: 14px;
    padding: 20px 22px;
    margin-top: 14px;
}

.result-rejected {
    background: #150a0a;
    border: 1px solid #4a1515;
    border-radius: 14px;
    padding: 20px 22px;
    margin-top: 14px;
}

.result-main {
    font-family: 'Fraunces', serif;
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 4px;
    line-height: 1;
}

.footer-note {
    text-align: center;
    font-size: 0.7rem;
    color: #2a3050;
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px solid #161c30;
}

</style>
""", unsafe_allow_html=True)

pipe = joblib.load("models/loan_model.pkl")
email = st.session_state.get("email", "")

# ───────── NAVBAR ─────────

st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)

col_logo, col_hist, col_logout = st.columns([6, 1.3, 1.3])

with col_logo:
    st.markdown(f"""
    <div class="nav-left">
        <div class="nav-logo">Loan<em>Sense</em></div>
        <div class="nav-dot"></div>
        <div class="nav-email">{email}</div>
    </div>
    """, unsafe_allow_html=True)

with col_hist:
    if st.button("History", key="nav_history", use_container_width=True):
        st.session_state["page"] = "dashboard"
        st.rerun()

with col_logout:
    if st.button("Logout", key="nav_logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ───────── HERO ─────────

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Credit Assessment Portal</div>
    <div class="hero-title">Loan <strong>Eligibility</strong><br>Assessment</div>
    <div class="hero-sub">
        Enter applicant details — instant AI-driven decision with credit risk profile
    </div>
</div>
""", unsafe_allow_html=True)

# ───────── FORM ─────────

st.markdown('<div class="section"><div class="section-label">Personal Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])

with col2:
    married = st.selectbox("Marital Status", ["Yes", "No"])
    self_employed = st.selectbox(
        "Employment Type",
        ["No", "Yes"],
        format_func=lambda x: "Salaried" if x == "No" else "Self Employed"
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section"><div class="section-label">Financial Details</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    applicant_income = st.number_input(
        "Monthly Income (₹)",
        min_value=0,
        value=5000,
        step=500
    )

with col4:
    loan_amount = st.number_input(
        "Loan Amount (₹ thousands)",
        min_value=0,
        value=120,
        step=10
    )

credit_history = st.selectbox(
    "Credit History",
    [1, 0],
    format_func=lambda x:
        "Clean — No previous defaults"
        if x == 1 else
        "Defaulted — Past dues recorded"
)

st.markdown('</div>', unsafe_allow_html=True)

# ───────── BUTTON ─────────

st.markdown('<div class="predict-btn">', unsafe_allow_html=True)

predict_clicked = st.button(
    "RUN CREDIT ASSESSMENT →",
    key="predict_btn"
)

st.markdown('</div>', unsafe_allow_html=True)

# ───────── PREDICTION ─────────

if predict_clicked:

    ratio = round(applicant_income / loan_amount, 2) if loan_amount > 0 else 0

    new_customer = {
        "ApplicantIncome": applicant_income,
        "LoanAmount": loan_amount,
        "Income_Loan_Ratio": ratio,
        "Credit_History": credit_history,
        "Gender_Male": 1 if gender == "Male" else 0,
        "Married_Yes": 1 if married == "Yes" else 0,
        "Education_Not Graduate": 1 if education == "Not Graduate" else 0,
        "Self_Employed_Yes": 1 if self_employed == "Yes" else 0
    }

    new_df = pd.DataFrame([new_customer])
    new_df = new_df.reindex(columns=pipe.feature_names_in_, fill_value=0)

    prob = pipe.predict_proba(new_df)[0][1]

    decision = "APPROVED" if prob >= 0.5 else "REJECTED"

    bar_width = round(prob * 100, 1)

    if decision == "APPROVED":

        st.markdown(f"""
        <div class="result-approved">
            <div style="font-size:0.62rem;font-weight:600;
            letter-spacing:3px;text-transform:uppercase;
            color:#34d399;margin-bottom:8px">
            Decision
            </div>

            <div class="result-main" style="color:#34d399">
            ✓ Loan Approved
            </div>

            <div style="font-size:0.78rem;color:#34d399;opacity:0.7">
            Approval Confidence — {bar_width}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class="result-rejected">
            <div style="font-size:0.62rem;font-weight:600;
            letter-spacing:3px;text-transform:uppercase;
            color:#f87171;margin-bottom:8px">
            Decision
            </div>

            <div class="result-main" style="color:#f87171">
            ✗ Loan Rejected
            </div>

            <div style="font-size:0.78rem;color:#f87171;opacity:0.7">
            Approval Confidence — {bar_width}%
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-note">
LoanSense AI · Powered by Machine Learning ·
For internal assessment use only
</div>
""", unsafe_allow_html=True)