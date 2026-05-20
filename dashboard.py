import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

def init_firebase():
    if not firebase_admin._apps:
        key_dict = {
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
        }
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
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&family=Geist:wght@300;400;500;600&display=swap');

    .dash-title {
        font-family: 'Fraunces', serif;
        font-size: 1.75rem;
        color: #eef0f8;
        font-weight: 600;
        margin-bottom: 0.3rem;
        margin-top: 1.5rem;
    }
    .dash-sub {
        font-size: 0.8rem;
        color: #4a5580;
        margin-bottom: 1.5rem;
    }
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
    .history-label {
        font-size: 0.65rem;
        color: #4a5580;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 3px;
    }
    .history-value {
        font-size: 0.9rem;
        color: #eef0f8;
        font-weight: 500;
    }
    .history-date {
        font-size: 0.7rem;
        color: #4a5580;
        margin-top: 3px;
    }
    .badge-approved {
        background: #0d1a12;
        color: #34d399;
        border: 1px solid #0d4429;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .badge-rejected {
        background: #150a0a;
        color: #f87171;
        border: 1px solid #4a1515;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .empty-state {
        text-align: center;
        color: #4a5580;
        padding: 3rem;
        font-size: 0.875rem;
        background: #0f1528;
        border: 1px solid #1e2540;
        border-radius: 14px;
        margin-top: 1rem;
    }
    .stats-row {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 12px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: #0f1528;
        border: 1px solid #1e2540;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .stat-label {
        font-size: 0.62rem;
        color: #4a5580;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .stat-value {
        font-family: 'Fraunces', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #eef0f8;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dash-title">Loan History</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dash-sub">Previous assessments for {user_email}</div>', unsafe_allow_html=True)

    docs = db.collection("predictions")\
             .where("email", "==", user_email)\
             .limit(10)\
             .stream()

    records = list(docs)
    records.sort(key=lambda x: x.to_dict().get("timestamp") or 0, reverse=True)

    if not records:
        st.markdown("""
        <div class="empty-state">
            📋 Koi previous assessment nahi mila<br><br>
            Pehla loan assessment karo!
        </div>
        """, unsafe_allow_html=True)
    else:
        total = len(records)
        approved = sum(1 for r in records if r.to_dict().get("decision") == "APPROVED")
        rejected = total - approved

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-label">Total</div>
                <div class="stat-value" style="color:#6c8fff">{total}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Approved</div>
                <div class="stat-value" style="color:#34d399">{approved}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Rejected</div>
                <div class="stat-value" style="color:#f87171">{rejected}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for doc in records:
            d = doc.to_dict()
            badge = 'badge-approved' if d["decision"] == "APPROVED" else 'badge-rejected'
            decision_text = "✓ Approved" if d["decision"] == "APPROVED" else "✗ Rejected"
            ts = d.get("timestamp")
            date_str = ts.strftime("%d %b %Y, %I:%M %p") if ts else "—"
            risk = d.get("risk", "N/A")

            st.markdown(f"""
            <div class="history-card">
                <div>
                    <div class="history-label">Income / Loan Amount</div>
                    <div class="history-value">₹{d['income']:,} / ₹{d['loan_amount']:,}</div>
                    <div class="history-date">{date_str}</div>
                </div>
                <div style="text-align:right">
                    <div class="history-label">Risk Level</div>
                    <div class="history-value" style="margin-bottom:6px">{risk}</div>
                    <div class="{badge}">{decision_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)