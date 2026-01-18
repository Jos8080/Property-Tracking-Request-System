import streamlit as st
import pandas as pd
from gspread_pandas import Spread
from datetime import datetime
import json

# የዲፓርትመንት ስም እና ርዕስ
st.set_page_config(page_title="Inventory Management System", layout="wide")
st.title("ዲጂታል የንብረት ቁጥጥር እና ጥያቄ ማቅረቢያ")

# በ Secrets ውስጥ ያስገባሽውን ቁልፍ ለአፑ ማስተዋወቅ
try:
    creds_dict = dict(st.secrets["gcp_service_account"])
    # 'Inventory_Database' የጎግል ሺቱ ስም መሆኑን አረጋግጪ
    spread = Spread('Inventory_Database', config=creds_dict)
    
    # ዳታውን ከሺቱ ላይ ማንበብ (Sheet names: Items, Trainers, Requests)
    items_df = spread.sheet_to_df(sheet='Items', index=0)
    trainers_df = spread.sheet_to_df(sheet='Trainers', index=0)
    trainers_list = trainers_df['FullName'].tolist()
    
except Exception as e:
    st.error(f"ከጎግል ሺት ጋር መገናኘት አልተቻለም። ስህተቱ፡ {e}")
    st.stop()

# የጎን ማውጫ (User Roles)
role = st.sidebar.selectbox("ተግባርዎን ይምረጡ", ["አሰልጣኝ", "አሲስታንት", "ሀላፊ"])

# --- 1. አሰልጣኝ ክፍል ---
if role == "አሰልጣኝ":
    st.subheader("የእቃ መጠየቂያ ፎርም")
    with st.form("request_form"):
        name = st.selectbox("ስምዎን ይምረጡ", trainers_list)
        item = st.selectbox("የሚፈልጉት እቃ", items_df['ItemName'].tolist())
        qty = st.number_input("ብዛት", min_value=1, step=1)
        submit = st.form_submit_button("ጥያቄ ላክ")
        
        if submit:
            new_req = pd.DataFrame([[name, item, qty, "Pending", str(datetime.now().date())]])
            spread.df_to_sheet(new_req, sheet='Requests', index=False, replace=False, add=True)
            st.success(f"ጥያቄዎ ተመዝግቧል! ለሀላፊው ተልኳል።")

# --- 2. አሲስታንት ክፍል ---
elif role == "አሲስታንት":
    st.subheader("አዲስ ንብረት ማስገቢያ")
    with st.form("add_item"):
        new_item = st.text_input("የእቃ ስም")
        total_qty = st.number_input("ጠቅላላ ብዛት", min_value=1)
        if st.form_submit_button("መዝግብ"):
            new_row = pd.DataFrame([[new_item, total_qty, total_qty]])
            spread.df_to_sheet(new_row, sheet='Items', index=False, replace=False, add=True)
            st.success("አዲስ እቃ ተጨምሯል!")
    
    st.divider()
    st.subheader("ያሉ እቃዎች ዝርዝር")
    st.dataframe(items_df)

# --- 3. ሀላፊ (Admin) ክፍል ---
else:
    st.subheader("የአስተዳደር እና የቁጥጥር ፓነል")
    requests_df = spread.sheet_to_df(sheet='Requests', index=0)
    
    st.write("### የጥያቄዎች እና የርክክብ ታሪክ")
    st.dataframe(requests_df)
    
    st.write("### የክምችት ሁኔታ")
    st.table(items_df)
