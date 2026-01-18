import streamlit as st
import pandas as pd
from gspread_pandas import Spread
from datetime import datetime

st.set_page_config(page_title="Inventory System", layout="wide")
st.title("ዲጂታል የንብረት ቁጥጥር እና ጥያቄ ማቅረቢያ")

# በከፍተኛ ጥንቃቄ ከ Secrets ቁልፉን መውሰድ
try:
    # ሙሉውን የሰርቪስ አካውንት መረጃ ከ Secrets መውሰድ
    s_account = st.secrets["gcp_service_account"]
    
    # ዲክሽነሪ መፍጠር (ይህ Base64 ስህተትን ይከላከላል)
    # app.py ውስጥ ያለው Credential ክፍል እንዲህ መሆን አለበት
s_account = st.secrets["gcp_service_account"]
creds_dict = {
    "type": s_account["type"],
    "project_id": s_account["project_id"],
    "private_key_id": s_account["private_key_id"],
    "private_key": s_account["private_key"].replace("\\n", "\n"), # ይህ መስመር ወሳኝ ነው!
    "client_email": s_account["client_email"],
    "client_id": s_account["client_id"],
    "auth_uri": s_account["auth_uri"],
    "token_uri": s_account["token_uri"],
    "auth_provider_x509_cert_url": s_account["auth_provider_x509_cert_url"],
    "client_x509_cert_url": s_account["client_x509_cert_url"]
}

spread = Spread('Inventory_Database', config=creds_dict)

    # ከጎግል ሺት ጋር መገናኘት
    spread = Spread('Inventory_Database', config=creds_dict)
    
    # ዳታውን ማንበብ
    items_df = spread.sheet_to_df(sheet='Items', index=0)
    trainers_df = spread.sheet_to_df(sheet='Trainers', index=0)
    trainers_list = trainers_df['FullName'].tolist()

    role = st.sidebar.selectbox("ተግባርዎን ይምረጡ", ["አሰልጣኝ", "አሲስታንት", "ሀላፊ"])

    if role == "አሰልጣኝ":
        st.subheader("የእቃ መጠየቂያ ፎርም")
        with st.form("request"):
            name = st.selectbox("ስምዎን ይምረጡ", trainers_list)
            item = st.selectbox("እቃ ይምረጡ", items_df['ItemName'].tolist())
            qty = st.number_input("ብዛት", min_value=1)
            if st.form_submit_button("ጥያቄ ላክ"):
                new_req = pd.DataFrame([[name, item, qty, "Pending", str(datetime.now().date())]])
                spread.df_to_sheet(new_req, sheet='Requests', index=False, replace=False, add=True)
                st.success("ጥያቄዎ ተመዝግቧል!")

    elif role == "አሲስታንት":
        st.subheader("አዲስ ንብረት ማስገቢያ")
        with st.form("add"):
            new_i = st.text_input("የእቃ ስም")
            new_q = st.number_input("ብዛት", min_value=1)
            if st.form_submit_button("መዝግብ"):
                new_row = pd.DataFrame([[new_i, new_q, new_q]])
                spread.df_to_sheet(new_row, sheet='Items', index=False, replace=False, add=True)
                st.success("ተመዝግቧል!")

    else:
        st.subheader("የአስተዳደር ክፍል")
        reqs = spread.sheet_to_df(sheet='Requests', index=0)
        st.write("የጥያቄዎች ታሪክ")
        st.dataframe(reqs)
        st.write("የክምችት ሁኔታ")
        st.table(items_df)

except Exception as e:
    st.error(f"ስህተት ተፈጥሯል፡ {e}")

