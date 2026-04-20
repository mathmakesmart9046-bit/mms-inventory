import streamlit as st
import json
from google.oauth2 import service_account
from google.cloud import firestore

# Simple Connection (Secrets se)
import streamlit as st
import json
from google.oauth2 import service_account
from google.cloud import firestore

# Mazboot Connection Logic
if "firebase" in st.secrets:
    key_dict = json.loads(st.secrets["firebase"]["key"])
    
    # Ye line private key ke format ko khud theek karegi
    if "private_key" in key_dict:
        key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
    
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project=key_dict['project_id'])
else:
    st.error("Secrets missing!")
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project=key_dict['project_id'])

st.title("MMS IT Inventory Dashboard")
# Yahan se aapka dashboard ka baaki code shuru ho jayega...
