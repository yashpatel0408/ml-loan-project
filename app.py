import streamlit as st
import pandas as pd
import joblib
from auth import show_auth_page
from dashboard import save_prediction, show_dashboard

# ─────────────────────────────────────────────
# AUTH CHECK
# ─────────────────────────────────────────────

if "user" not in st.session_state:
    show_auth_page()
    st.stop()

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="LoanSense AI",
    page_icon="🏦",
    layout="wide"
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

if "page" not in st.session_state:
    st.session_state.page = "main"

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@300;600&family=Geist:wght@300;400;500;600&display=swap');

html, body, .stApp {
    background: #0c0f1a !important;
    color: #eef0f8 !important;
    font-family: 'Geist', sans-serif !important;
}

header[data-testid="stHeader"] {
    display: none !important;
}

.block-container {
    max-width: 760px !important;
    padding-top: 0rem !important;
}

/* ───────── NAVBAR ───────── */

.nav-wrapper {
    background: #080b14;
    border-bottom: 1px solid #161c30;
    padding: 12px 18px;
    margin: -1rem -1rem 1.5rem -1rem;
}

.nav-logo {
    font-family: 'Fraunces', serif;
    font-size: 1.25rem;
    color: #eef0f8;
    font-weight: 600;
}

.nav-logo em {
    color: #6c8fff;
    font-style: italic;
}

.nav-email {
    font-size: 0.72rem;
    color: #5b6487;
}

div[data-testid="column"]:nth-of-type(2) button,
div[data-testid="column"]:nth-of-type(3) button {

    width: 100% !important;
    height: 42px !important;

    background: transparent !important;
    border: 1px solid #1e2540 !important;
    border-radius: 10px !important;

    color: #c7d2fe !important;

    font-size: 0.72rem !important;
    font-weight: 600 !important;

    letter-spacing: 1px !important;
    text-transform: uppercase !important;

    white-space: nowrap !important;
}

div[data-testid="column"]:nth-of-type(2) button:hover {
    border-color: #6c8fff !important;
    color: white !important;
}

div[data-testid="column"]:nth-of-type(3) button:hover {
    border-color: #ef4444 !important;
    color: #ef4444 !important;
}

/* ───────── HERO ───────── */

.hero {
    background: linear-gradient(180deg, #111827 0%, #0c0f1a 100%);
    padding: 28px 20px 24px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid #1e2540;
}

.hero-small {
    color: #6c8fff;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 0.65rem;
    font-weight: 600;
}

.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 2rem;
    margin-top: 10px;
    line-height: 1.2;
}

.hero-sub {
    color: #667085;
    margin-top: 10px;
    font-size: 0.85rem;
}

/* ───────── CARD ───────── */

.card {
    background: #111827;
    border: 1px solid #1e2540;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 18px;
}

.card-title {
    color: #6b7280;
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
    font-weight: 600;
}

/* ───────── INPUTS ───────── */

label {
    color: #9ca3af !important;
}

.stSelectbox div[data-baseweb="select"],
.stNumberInput input {
    background: #0b1220 !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: white !important;
}

/* ───────── BUTTON ───────── */

.predict-btn button {
    width: 100% !important;
    background: #6c8fff !important;
    color: #0c0f1a !important;
    border: none !important;
    border-radius: 12px !important;
    height: 52px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
}

.predict-btn button:hover {
    opacity: 0.9;
}

/* ───────── RESULT ───────── */

.result-box {
    border-radius: 18px;
    padding: 22px;
    margin-top: 18px;
}

.approved {
    background: #07130c;
    border: 1px solid #14532d;
}

.rejected {
    background: #160809;
    border: 1px solid #7f1d1d;
}

.result-title {
    font-size: 2rem;
    font-family: 'Fraunces', serif;
    font-weight: 600;
}

.footer-note {
    text-align: center;
    color: #394150;
    font-size: 0.72rem;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MODEL LOAD
# ─────────────────────────────────────────────

pipe = joblib.load("models/loan_model.pkl")

email = st.session_state.get("email", "user@gmail.com")

# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────

st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([6, 1.5, 1.5])

with col1:
    st.markdown(f"""
    <div class="nav-logo">
        Loan<em>Sense</em>
    </div>

    <div class="nav-email">
        {email}
    </div>
    """, unsafe_allow_html=True)

with col2:

    if st.button("History", use_container_width=True):

        st.session_state.page = "dashboard"

        st.rerun()

with col3:

    if st.button("Logout", use_container_width=True):

        st.session_state.clear()

        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DASHBOARD / HISTORY PAGE
# ─────────────────────────────────────────────

if st.session_state.page == "dashboard":

    show_dashboard(email)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Back To Assessment"):

        st.session_state.page = "main"

        st.rerun()

    st.stop()

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero">

<div class="hero-small">
Credit Assessment Portal
</div>

<div class="hero-title">
Loan <strong>Eligibility</strong><br>
Assessment
</div>

<div class="hero-sub">
Enter applicant details — instant AI-driven decision with credit risk profile
</div>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PERSONAL INFO
# ─────────────────────────────────────────────

st.markdown("""
<div class="card">
<div class="card-title">Personal Information</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

with c2:

    married = st.selectbox(
        "Marital Status",
        ["Yes", "No"]
    )

    self_employed = st.selectbox(
        "Employment Type",
        ["No", "Yes"],
        format_func=lambda x:
        "Salaried" if x == "No"
        else "Self Employed"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FINANCIAL INFO
# ─────────────────────────────────────────────

st.markdown("""
<div class="card">
<div class="card-title">Financial Details</div>
""", unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:

    applicant_income = st.number_input(
        "Monthly Income (₹)",
        min_value=0,
        value=5000,
        step=500
    )

with c4:

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

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PREDICT BUTTON
# ─────────────────────────────────────────────

st.markdown('<div class="predict-btn">', unsafe_allow_html=True)

predict = st.button(
    "RUN CREDIT ASSESSMENT →",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────

if predict:

    ratio = round(
        applicant_income / loan_amount,
        2
    ) if loan_amount > 0 else 0

    customer = {

        "ApplicantIncome": applicant_income,

        "LoanAmount": loan_amount,

        "Income_Loan_Ratio": ratio,

        "Credit_History": credit_history,

        "Gender_Male":
        1 if gender == "Male" else 0,

        "Married_Yes":
        1 if married == "Yes" else 0,

        "Education_Not Graduate":
        1 if education == "Not Graduate" else 0,

        "Self_Employed_Yes":
        1 if self_employed == "Yes" else 0
    }

    df = pd.DataFrame([customer])

    # IMPORTANT FIX
    df = df.reindex(
        columns=pipe.feature_names_in_,
        fill_value=0
    )

    try:

        prob = pipe.predict_proba(df)[0][1]

    except Exception as e:

        st.error(f"Prediction Error: {e}")

        st.stop()

    # ───────── CUSTOM LOGIC ─────────

    if ratio >= 2.0 and credit_history == 1:

        prob = max(prob, 0.82)

    elif ratio >= 1.0 and credit_history == 1:

        prob = max(prob, 0.60)

    elif ratio < 0.5 or credit_history == 0:

        prob = min(prob, 0.35)

    # ───────── DECISION ─────────

    decision = (
        "APPROVED"
        if prob >= 0.5
        else "REJECTED"
    )

    confidence = round(prob * 100, 1)

    # ───────── SAVE HISTORY ─────────

    save_prediction(email, {
        "income": applicant_income,
        "loan_amount": loan_amount,
        "credit_history": credit_history,
        "decision": decision,
        "probability": confidence
    })

    # ───────── APPROVED ─────────

    if decision == "APPROVED":

        st.markdown(f"""
        <div class="result-box approved">

        <div style="
        color:#4ade80;
        text-transform:uppercase;
        letter-spacing:2px;
        font-size:0.7rem;
        margin-bottom:8px;">

        Decision

        </div>

        <div class="result-title"
        style="color:#4ade80;">

        ✓ Loan Approved

        </div>

        <div style="
        margin-top:8px;
        color:#86efac;">

        Approval Confidence — {confidence}%

        </div>

        </div>
        """, unsafe_allow_html=True)

    # ───────── REJECTED ─────────

    else:

        st.markdown(f"""
        <div class="result-box rejected">

        <div style="
        color:#f87171;
        text-transform:uppercase;
        letter-spacing:2px;
        font-size:0.7rem;
        margin-bottom:8px;">

        Decision

        </div>

        <div class="result-title"
        style="color:#f87171;">

        ✗ Loan Rejected

        </div>

        <div style="
        margin-top:8px;
        color:#fca5a5;">

        Approval Confidence — {confidence}%

        </div>

        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

st.markdown("""
<div class="footer-note">

LoanSense AI · Powered by Machine Learning ·
For internal assessment use only

</div>
""", unsafe_allow_html=True)