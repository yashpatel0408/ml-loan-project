import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

def init_firebase():
    if not firebase_admin._apps:
        key_dict = json.loads(json.dumps({
            "type": st.secrets["firebase_key"]["type"],
            "project_id": st.secrets["firebase_key"]["project_id"],
            "private_key_id": st.secrets["firebase_key"]["private_key_id"],
            "private_key": st.secrets["firebase_key"]["private_key"],
            "client_email": st.secrets["firebase_key"]["client_email"],
            "client_id": st.secrets["firebase_key"]["client_id"],
            "auth_uri": st.secrets["firebase_key"]["auth_uri"],
            "token_uri": st.secrets["firebase_key"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase_key"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase_key"]["client_x509_cert_url"],
            "universe_domain": st.secrets["firebase_key"]["universe_domain"]
        }))
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def save_prediction(user_email, data):
    db = init_firebase()
    db.collection("predictions").add({
        "email": user_email,
        "income": data["income"],
        "loan_amount": data["loan_amount"],
        "credit_history": data["credit_history"],
        "decision": data["decision"],
        "probability": data["probability"],
        "risk": data["risk"],
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def show_dashboard(user_email):
    db = init_firebase()

    st.markdown("""
    <style>
    .dash-title {
        font-family: 'Fraunces', serif;
        font-size: 1.4rem;
        color: #eef0f8;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .dash-sub { font-size: 0.8rem; color: #4a5580; margin-bottom: 1.5rem; }
    .history-card {
        background: #0f1528;
        border: 1px solid #1e2540;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .history-label { font-size: 0.7rem; color: #4a5580; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px; }
    .history-value { font-size: 0.9rem; color: #eef0f8; font-weight: 500; }
    .badge-approved { background: #0d1a12; color: #34d399; border: 1px solid #0d4429; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
    .badge-rejected { background: #150a0a; color: #f87171; border: 1px solid #4a1515; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }
    .empty-state { text-align: center; color: #4a5580; padding: 3rem; font-size: 0.875rem; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dash-title">Loan History</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-sub">Previous assessments for {user_email}</div>', unsafe_allow_html=True)

    docs = db.collection("predictions")\
             .where("email", "==", user_email)\
             .order_by("timestamp", direction=firestore.Query.DESCENDING)\
             .limit(10)\
             .stream()

    records = list(docs)

    if not records:
        st.markdown('<div class="empty-state">📋 Koi previous loan assessment nahi mila<br>Pehla assessment karo!</div>', unsafe_allow_html=True)
    else:
        for doc in records:
            d = doc.to_dict()
            badge = 'badge-approved' if d["decision"] == "APPROVED" else 'badge-rejected'
            decision_text = "✓ Approved" if d["decision"] == "APPROVED" else "✗ Rejected"
            ts = d.get("timestamp")
            date_str = ts.strftime("%d %b %Y, %I:%M %p") if ts else "—"

            st.markdown(f"""
            <div class="history-card">
                <div>
                    <div class="history-label">Income / Loan</div>
                    <div class="history-value">₹{d['income']:,} / ₹{d['loan_amount']:,}k</div>
                    <div style="font-size:0.72rem;color:#4a5580;margin-top:3px">{date_str}</div>
                </div>
                <div style="text-align:right">
                    <div class="history-label">Risk</div>
                    <div class="history-value" style="margin-bottom:6px">{d.get('risk','—')}</div>
                    <div class="{badge}">{decision_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)