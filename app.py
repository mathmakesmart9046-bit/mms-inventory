import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime

# --- Firebase Setup ---
import streamlit as st
import json
from google.oauth2 import service_account
from google.cloud import firestore

# Naya tareeqa: Secrets se key uthayen
key_dict = json.loads(st.secrets["firebase"]["key"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project=key_dict['project_id'])
db = firestore.client()

st.set_page_config(page_title="MMS IT Inventory System", layout="wide")

# --- Session States ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# --- Helper Functions ---
def add_log(action):
    log_data = {
        "user": st.session_state.username,
        "action": action,
        "timestamp": datetime.now()
    }
    db.collection("activity_logs").add(log_data)

# --- Authentication Logic ---
def login_page():
    st.title("🖥️ MMS IT Management System")
    with st.container():
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        if st.button("Login"):
            user_ref = db.collection("users").document(user_input).get()
            if user_ref.exists:
                data = user_ref.to_dict()
                if data['password'] == pass_input:
                    st.session_state.logged_in = True
                    st.session_state.username = user_input
                    st.session_state.role = data.get('role', 'staff')
                    add_log("User Logged In")
                    st.rerun()
                else:
                    st.error("Authentication Failed: Incorrect Password.")
            else:
                st.error("Authentication Failed: Username not found.")

if not st.session_state.logged_in:
    login_page()
else:
    # --- Sidebar ---
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    options = ["Inventory Dashboard", "Add/Edit Item", "History Logs", "My Settings"]
    if st.session_state.role == "admin":
        options.append("User Management")
    
    menu = st.sidebar.selectbox("Main Menu", options)
    
    if st.sidebar.button("Logout"):
        add_log("User Logged Out")
        st.session_state.logged_in = False
        st.rerun()

    # --- 1. Inventory Dashboard ---
    if menu == "Inventory Dashboard":
        st.header("📦 Current Inventory")
        docs = db.collection("it_inventory").stream()
        items = [doc.to_dict() for doc in docs]
        if items:
            df = pd.DataFrame(items)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Inventory is empty.")

    # --- 2. Add/Edit Item ---
    elif menu == "Add/Edit Item":
        st.header("📝 Manage Items")
        with st.form("inventory_form"):
            brand = st.text_input("Brand")
            model = st.text_input("Model")
            serial = st.text_input("Serial Number")
            assigned = st.text_input("Assigned To")
            if st.form_submit_button("Save Item"):
                item_data = {
                    "brand": brand, "model": model, "serial": serial, 
                    "assigned": assigned, "last_updated_by": st.session_state.username
                }
                db.collection("it_inventory").document(serial).set(item_data)
                add_log(f"Added/Updated Item: {serial}")
                st.success(f"Success: Item {serial} has been saved.")

    # --- 3. History Logs ---
    elif menu == "History Logs":
        st.header("📜 System Activity Logs")
        logs = db.collection("activity_logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
        log_list = [{"Time": l.to_dict()['timestamp'], "User": l.to_dict()['user'], "Action": l.to_dict()['action']} for l in logs]
        st.table(pd.DataFrame(log_list))

    # --- 4. User Management (Admin Only) ---
    elif menu == "User Management":
        st.header("👥 User Administration")
        with st.expander("Create New User"):
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
            new_role = st.selectbox("Role", ["staff", "admin"])
            if st.button("Create User"):
                db.collection("users").document(new_user).set({"password": new_pass, "role": new_role})
                add_log(f"Created new user: {new_user}")
                st.success(f"Success: User {new_user} created.")

    # --- 5. My Settings ---
    elif menu == "My Settings":
        st.header("⚙️ Account Settings")
        curr_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Update Password"):
            user_ref = db.collection("users").document(st.session_state.username)
            if user_ref.get().to_dict()['password'] == curr_pass:
                user_ref.update({"password": new_pass})
                add_log("Changed Password")
                st.success("Success: Password updated successfully.")
            else:
                st.error("Error: Current password does not match.")
