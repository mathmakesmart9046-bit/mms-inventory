import streamlit as st
import json
from google.oauth2 import service_account
from google.cloud import firestore

# Simple Connection (Secrets se)
key_dict = json.loads(st.secrets["firebase"]["key"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project=key_dict['project_id'])

st.title("MMS IT Inventory Dashboard")
# Yahan se aapka dashboard ka baaki code shuru ho jayega...
