import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Page Configuration (Ye hamesha sab se upar hona chahiye)
st.set_page_config(page_title="MMS IT Inventory System", layout="wide")

# 2. Firebase Setup (Secrets se connect karne ke liye)
if not firebase_admin._apps:
    try:
        # Streamlit Secrets se JSON string utha kar convert karna
        key_dict = json.loads(st.secrets["firebase"]["key"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Firebase setup mein masla hai: {e}")
        st.stop() # Agar connect na ho to app yahan ruk jaye

# Firestore database client initialize karein
db = firestore.client()

# 3. Session States (Login handle karne ke liye)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# 4. Helper Functions
def add_log(action):
    """Activity log ko Firestore mein save karne ke liye"""
    try:
        log_data = {
            "user": st.session_state.get("username", "Unknown"),
            "action": action,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        db.collection("logs").add(log_data)
    except Exception as e:
        print(f"Log save nahi ho saka: {e}")

# --- Yahan se aapki app ka baaki UI shuru hoga ---

st.title("MMS IT Inventory Management System")

if not st.session_state.logged_in:
    st.subheader("Please Login")
    # Login ka code yahan aayega...
else:
    st.success(f"Welcome, {st.session_state.username}")
    # Inventory ka main code yahan aayega...