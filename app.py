import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="LoanSense AI", page_icon="🏦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&family=Geist:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Geist', sans-serif !important;
    background-color: #0c0f1a !important;
    color: #eef0f8 !important;
}
.stApp { background: #0c0f1a !important; }

.nav {
    background: #080b14;
    border-bottom: 1px solid #161c30;
    padding: 13px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1rem 0 -1rem;
}
.nav-logo { font-family: 'Fraunces', serif; font-size: 1.25rem; color: #eef0f8; font-weight: 600; letter-spacing: -0.5px; }
.nav-logo em { font-style: italic; color: #6c8fff; }
.nav-right { display: flex; align-items: center; gap: 10px; }
.nav-dot { width: 6px; height: 6px; border-radius: 50%; background: #6c8fff; opacity: 0.7; }
.nav-tag { font-size: 0.65rem; color: #4a5580; font-weight: 500; letter-spacing: 1.5px; text-transform: uppercase; }

.hero {
    background: linear-gradient(180deg, #0f1528 0%, #0c0f1a 100%);
    padding: 26px 4px 20px;
    border-bottom: 1px solid #161c30;
    margin-bottom: 20px;
}
.hero-eyebrow { font-size: 0.62rem; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; color: #6c8fff; margin-bottom: 8px; }
.hero-title { font-family: 'Fraunces', serif; font-size: 1.75rem; color: #eef0f8; font-weight: 300; line-height: 1.2; margin-bottom: 6px; }
.hero-title strong { font-weight: 600; }
.hero-sub { font-size: 0.8rem; color: #4a5580; font-weight: 400; line-height: 1.5; }

.section {
    background: #0f1528;
    border: 1px solid #1e2540;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.section-head { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.section-label { font-size: 0.65rem; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; color: #4a5580; }

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

div.stButton > button {
    width: 100%;
    background: #6c8fff;
    color: #080b14;
    font-family: 'Geist', sans-serif;
    font-weight: 600;
    font-size: 0.8rem;
    border: none;
    border-radius: 10px;
    padding: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
    cursor: pointer;
    transition: opacity 0.2s;
}
div.stButton > button:hover { opacity: 0.85; }

.divider { height: 1px; background: #161c30; margin: 14px 0; }

.result-approved { background: #060f10; border: 1px solid #0d4429; border-radius: 14px; padding: 20px 22px; margin-top: 14px; }
.result-rejected { background: #150a0a; border: 1px solid #4a1515; border-radius: 14px; padding: 20px 22px; margin-top: 14px; }
.result-eyebrow { font-size: 0.62rem; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 8px; }
.result-main { font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 600; margin-bottom: 4px; line-height: 1; }

.risk-block {
    background: #0f1528;
    border: 1px solid #1e2540;
    border-radius: 14px;
    padding: 18px 20px;
    margin-top: 12px;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 14px;
    align-items: start;
}
.risk-left { display: flex; flex-direction: column; align-items: center; gap: 6px; }
.risk-circle { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.risk-level-tag { font-size: 0.58rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; }
.risk-right-eyebrow { font-size: 0.62rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #4a5580; margin-bottom: 4px; }
.risk-right-title { font-family: 'Fraunces', serif; font-size: 1.15rem; color: #eef0f8; font-weight: 600; margin-bottom: 5px; }
.risk-right-desc { font-size: 0.78rem; color: #6b7280; line-height: 1.5; margin-bottom: 10px; }
.risk-pills { display: flex; flex-wrap: wrap; gap: 6px; }
.pill { font-size: 0.7rem; font-weight: 500; padding: 4px 10px; border-radius: 6px; }

.suggestion-block { background: #0f1528; border: 1px solid #1e2540; border-radius: 14px; padding: 18px 20px; margin-top: 12px; }
.suggestion-eyebrow { font-size: 0.62rem; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: #f87171; margin-bottom: 12px; }
.suggestion-item { font-size: 0.82rem; color: #9ca3af; font-weight: 400; padding: 6px 0; border-bottom: 1px solid #161c30; }
.suggestion-item:last-child { border-bottom: none; }

.ratio-box {
    background: #080b14;
    border: 1px solid #1e2540;
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.ratio-label { font-size: 0.68rem; font-weight: 600; color: #4a5580; text-transform: uppercase; letter-spacing: 0.8px; }
.ratio-value { font-size: 0.9rem; font-weight: 600; }

.footer-note { text-align: center; font-size: 0.7rem; color: #2a3050; margin-top: 18px; padding-top: 14px; border-top: 1px solid #161c30; }
</style>
""", unsafe_allow_html=True)

pipe = joblib.load("models/loan_model.pkl")

st.markdown("""
<div class="nav">
    <div class="nav-logo">Loan<em>Sense</em></div>
    <div class="nav-right">
        <div class="nav-dot"></div>
        <div class="nav-tag">AI Credit Engine</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Credit Assessment Portal</div>
    <div class="hero-title">Loan <strong>Eligibility</strong><br>Assessment</div>
    <div class="hero-sub">Enter applicant details — instant AI-driven decision with credit risk profile</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section"><div class="section-head"><div class="section-label">Personal Information</div></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
with col2:
    married = st.selectbox("Marital Status", ["Yes", "No"])
    self_employed = st.selectbox("Employment Type", ["No", "Yes"], format_func=lambda x: "Salaried" if x == "No" else "Self Employed")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section"><div class="section-head"><div class="section-label">Financial Details</div></div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    applicant_income = st.number_input("Monthly Income (₹)", min_value=0, value=5000, step=500)
with col4:
    loan_amount = st.number_input("Loan Amount (₹ thousands)", min_value=0, value=120, step=10)

credit_history = st.selectbox("Credit History", [1, 0],
    format_func=lambda x: "Clean — No previous defaults" if x == 1 else "Defaulted — Past dues recorded")

ratio = round(applicant_income / loan_amount, 2) if loan_amount > 0 else 0
ratio_color = "#34d399" if ratio >= 2.0 else "#fcd34d" if ratio >= 1.0 else "#f87171"
st.markdown(f"""
<div class="ratio-box">
    <div class="ratio-label">Income / Loan Ratio</div>
    <div class="ratio-value" style="color:{ratio_color}">{ratio}x</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("RUN CREDIT ASSESSMENT →"):
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

    # Business Rule Override
    if ratio >= 2.0 and credit_history == 1:
        prob = max(prob, 0.82)
    elif ratio >= 1.0 and credit_history == 1:
        prob = max(prob, 0.60)
    elif ratio < 0.5 or credit_history == 0:
        prob = min(prob, 0.35)

    decision = "APPROVED" if prob >= 0.5 else "REJECTED"
    bar_width = round(prob * 100, 1)

    if decision == "APPROVED":
        st.markdown(f"""
        <div class="result-approved">
            <div class="result-eyebrow" style="color:#34d399">Decision</div>
            <div class="result-main" style="color:#34d399">✓ Loan Approved</div>
            <div class="result-conf" style="color:#34d399; opacity:0.7">Approval Confidence — {bar_width}%</div>
            <div style="margin-top:14px">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                    <span style="font-size:0.7rem;color:#4a5580;font-weight:500">Confidence Score</span>
                    <strong style="font-size:0.7rem;color:#34d399">{bar_width}%</strong>
                </div>
                <div style="background:#0d1a12;border-radius:999px;height:5px;overflow:hidden">
                    <div style="background:linear-gradient(90deg,#059669,#34d399);height:100%;width:{bar_width}%;border-radius:999px"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if prob >= 0.80:
            circle_bg, circle_border, tag_color, risk_title, risk_desc, pills, pill_bg, pill_color, pill_border = (
                "#0f1f0f", "#15803d", "#15803d",
                "Low Risk Profile",
                "Strong repayment profile. High confidence in timely loan servicing throughout tenure.",
                ["Standard interest rate", "No collateral needed", "Annual review"],
                "#0d1a12", "#34d399", "#0d4429"
            )
            emoji = "🟢"
        elif prob >= 0.60:
            circle_bg, circle_border, tag_color, risk_title, risk_desc, pills, pill_bg, pill_color, pill_border = (
                "#1a1200", "#b45309", "#d97706",
                "Medium Risk Profile",
                "Moderate repayment profile. Loan serviceable with standard monitoring through tenure.",
                ["+0.5% risk premium", "Quarterly review", "No collateral needed"],
                "#1a1200", "#fcd34d", "#78350f"
            )
            emoji = "🟡"
        else:
            circle_bg, circle_border, tag_color, risk_title, risk_desc, pills, pill_bg, pill_color, pill_border = (
                "#1a0a0a", "#b91c1c", "#ef4444",
                "High Risk Profile",
                "Weak repayment profile. Elevated risk — close monitoring and security required.",
                ["+1.5% risk premium", "Monthly review", "Collateral required"],
                "#1a0a0a", "#f87171", "#7f1d1d"
            )
            emoji = "🔴"

        pills_html = "".join([f'<div class="pill" style="background:{pill_bg};color:{pill_color};border:1px solid {pill_border}">{p}</div>' for p in pills])

        st.markdown(f"""
        <div class="risk-block">
            <div class="risk-left">
                <div class="risk-circle" style="background:{circle_bg};border:1.5px solid {circle_border}">{emoji}</div>
                <div class="risk-level-tag" style="color:{tag_color}">{risk_title.split()[0]}</div>
            </div>
            <div>
                <div class="risk-right-eyebrow">Credit Risk Assignment</div>
                <div class="risk-right-title">{risk_title}</div>
                <div class="risk-right-desc">{risk_desc}</div>
                <div class="risk-pills">{pills_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class="result-rejected">
            <div class="result-eyebrow" style="color:#f87171">Decision</div>
            <div class="result-main" style="color:#f87171">✗ Loan Rejected</div>
            <div class="result-conf" style="color:#f87171; opacity:0.7">Approval Confidence — {bar_width}%</div>
            <div style="margin-top:14px">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                    <span style="font-size:0.7rem;color:#4a5580;font-weight:500">Confidence Score</span>
                    <strong style="font-size:0.7rem;color:#f87171">{bar_width}%</strong>
                </div>
                <div style="background:#1a0a0a;border-radius:999px;height:5px;overflow:hidden">
                    <div style="background:linear-gradient(90deg,#991b1b,#f87171);height:100%;width:{bar_width}%;border-radius:999px"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="suggestion-block">
            <div class="suggestion-eyebrow">Recommendations to Improve Eligibility</div>
            <div class="suggestion-item">→ Maintain a clean credit record for at least 6 months</div>
            <div class="suggestion-item">→ Increase monthly income or add a co-applicant</div>
            <div class="suggestion-item">→ Reduce the requested loan amount</div>
            <div class="suggestion-item">→ Reapply after addressing the above factors</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footer-note">LoanSense AI · Powered by Machine Learning · For internal assessment use only</div>', unsafe_allow_html=True)