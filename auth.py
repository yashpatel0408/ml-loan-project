import streamlit as st
import requests
import json

FIREBASE_API_KEY = st.secrets["FIREBASE_API_KEY"]

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    return r.json()

def signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    return r.json()

def show_auth_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&family=Geist:wght@300;400;500;600&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Geist', sans-serif !important;
        background-color: #0c0f1a !important;
        color: #eef0f8 !important;
    }
    .stApp { background: #0c0f1a !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .block-container {
        max-width: 420px !important;
        margin: 0 auto !important;
        padding-top: 4rem !important;
    }
    .auth-logo {
        font-family: 'Fraunces', serif;
        font-size: 2rem;
        color: #eef0f8;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .auth-logo em { font-style: italic; color: #6c8fff; }
    .auth-sub {
        text-align: center;
        color: #4a5580;
        font-size: 0.82rem;
        margin-bottom: 2rem;
    }
    .auth-card {
        background: #0f1528;
        border: 1px solid #1e2540;
        border-radius: 16px;
        padding: 2rem;
    }
    div[data-testid="stTextInput"] label {
        color: #4a5580 !important;
        font-size: 0.68rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stTextInput"] input {
        background: #080b14 !important;
        border: 1px solid #1e2540 !important;
        border-radius: 8px !important;
        color: #eef0f8 !important;
        font-size: 0.875rem !important;
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
        margin-top: 0.5rem;
    }
    div.stButton > button:hover { opacity: 0.85; }
    .error-box {
        background: #150a0a;
        border: 1px solid #4a1515;
        border-radius: 8px;
        padding: 10px 14px;
        color: #f87171;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    .success-box {
        background: #060f10;
        border: 1px solid #0d4429;
        border-radius: 8px;
        padding: 10px 14px;
        color: #34d399;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-logo">Loan<em>Sense</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">AI-Powered Credit Assessment Portal</div>', unsafe_allow_html=True)

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
        if st.button("LOGIN →", key="login_btn"):
            if email and password:
                result = login(email, password)
                if "idToken" in result:
                    st.session_state["user"] = result
                    st.session_state["email"] = email
                    st.rerun()
                else:
                    error = result.get("error", {}).get("message", "Login failed")
                    st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">❌ Email aur password dono bharo</div>', unsafe_allow_html=True)

    with tab2:
        new_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
        new_password = st.text_input("Password", type="password", key="signup_pass", placeholder="Min 6 characters")
        if st.button("CREATE ACCOUNT →", key="signup_btn"):
            if new_email and new_password:
                result = signup(new_email, new_password)
                if "idToken" in result:
                    st.session_state["user"] = result
                    st.session_state["email"] = new_email
                    st.rerun()
                else:
                    error = result.get("error", {}).get("message", "Signup failed")
                    st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">❌ Email aur password dono bharo</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)