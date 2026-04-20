import streamlit as st
import json
from google.oauth2 import service_account
from google.cloud import firestore

# Naya tareeqa jo Secrets se key uthaye ga
if "firebase" in st.secrets:
    key_dict = json.loads(st.secrets["firebase"]["key"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project=key_dict['project_id'])
else:
    st.error("Firebase setup mein masla hai: 'st.secrets' mein key nahi mili.")
