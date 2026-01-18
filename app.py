import streamlit as st
import pandas as pd
from gspread_pandas import Spread
from datetime import datetime
import json

st.set_page_config(page_title="Inventory System", layout="wide")
st.title("ዲጂታል የንብረት ቁጥጥር እና ጥያቄ ማቅረቢያ")

# ምስጢራዊ ቁልፉን ከ Secrets ላይ በንጽህና መቀበል
try:
    # በ Secrets ውስጥ 'gcp_service_account' በሚል የተቀመጠውን ዳታ ማንበብ
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # ሰረዞችን ማስተካከል (ይህ የ Base64 ስህተትን ይከላከላል)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
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
