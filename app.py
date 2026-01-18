import streamlit as st
import pandas as pd
from gspread_pandas import Spread
from datetime import datetime

st.set_page_config(page_title="Inventory System", layout="wide")
st.title("ዲጂታል የንብረት ቁጥጥር እና ጥያቄ ማቅረቢያ")

# ምስጢራዊ ቁልፉን ለማስተካከል የሚረዳ ፋንክሽን
def get_creds():
    # ቁልፉን ያለምንም የዝላይ ምልክት በአንድ መስመር እናስቀምጠው
    raw_key = ("-----BEGIN PRIVATE KEY-----\n"
               "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDztluqjHfDZqQn\n"
               "FV31RAQ8Jyjw/nYZWTNh1n6k6YZG6OYK7iZmriipfwk0oOLjY4GcWbUY+8Q3x+bh\n"
               "OCXtJwT9OCYmk0I2XrnlrV3DbktlGWnUM0nFhYqT6Yi4lcwxgeggQnwp4l0hTSKh\n"
               "hSVMkt1eLaBgTJjccTEYsn5kkt02ug3///nQyv3LnjL5qxXqVZkqZjT0hpmUB2iA\n"
               "+6E4Wurv5mGx33gvl7+I6QrkbnoQoqhv9PTKvST70P4+oH06juitSqyAhe96s6C2\n"
               "CbfGHRUOv8P8PHxo4jO8SnQVNbEN5u4OYYS1CV6j516XfMZiQtNukDyfiZa7Qyil\n"
               "KddBLyK1AgMBAAECggEAFbV1+15pUaLMNv4IgU82eFw9oZ/tCauAL/QhElQJ5bmb\n"
               "ujgF/CoBzb1W5tT4+OvVcQWto8TTcOuR1ZiAilwqLdspTNDbukecVAjqG/0wYphN\n"
               "nrL0H0nwngK7yAo03Y+aQNIVvlXSIOq3qCoy3apd/eALk8QcJq8M6bhqCNze81EG4\n"
               "exGRq+VtDQMmrodP/gwnObHBjXMI/qEB/aQZxJhtHSUfOSudySwBOu+um9n8XQQR\n"
               "5H56WP7QnQ4n5nDLt7NVSl+eI/lFi5c95ChQfR+aPUox+V7G4ngvYW5yZdDzoO27\n"
               "N8m9niVRWjiLixYsJ8Zo026Q/nhB1pdFJimh2fwAeQKBgQD65MCgwaXzlKr/VA07\n"
               "q/d50Spgosw5g5jqVoNwS1K1heDzStVz0WaSt3ScO5X+8gYzMxZzpuwdaeKaIkND\n"
               "ZM6h4Qn/IVCts6r5TQxUS1yduwYPMDvEtN3nt2goD2rN4V3/0UPU85H9Qmb76vyp\n"
               "2yEgi/Est6uf0k4ZkYi7ZEo/HQKBgQD4rDBULp2U8dzLqi1yV1tySpOqhM/2z5tF\n"
               "n12FleZKX12dDHrRkCkF1fyGzIP3vMSnHgCu94pQB/LM2Smdk+Hj0E1T/EqlKg0Y\n"
               "RNt2VrvjuWZ8CbQHwZBsWu4fab/+El8+DKknEoqe6kr+kFDT6951HW6pxYqb+j3J\n"
               "6crr7U0meQKBgCN/5IWagNmzSnKwOOMdlPmmj+F2h4EHzsYxkY19CunmVIr4JrWp\n"
               "hmLyFEza3YFiS2BJNT8N+lC7H7YBbRUHGXmsNtbjpt+9EU8PCNSQiT1ELjpN79cI\n"
               "ZHGZ8OHiNJGG9t7whDGIeTqlf57bg/6go9JQGsLiBiWqAyT5A6jIKv09AoGBAKfI\n"
               "rncuWL7Vji+Q7EcY8CemcAn+wL78Bv0r8RMgOBj4TZaYhAn/5d39Kvzc4zH1mQ5V\n"
               "LQrhFN647jcPU4fx7tkig/pl4Qud2uYEF7u5+95ECwUoGuOc09B4bfCeDp/kT4Tz\n"
               "T/KADS36UY1/XDoRDLEiobdFBSgG6UfiSjtzirmpAoGBALTTamSXeZAqsIT7nPJh\n"
               "912FzAZv/H2iqeMn3sn0LaVFR2qIYcAFL2ZOCrPr+HNk6imkwfV7M3G3XXMjlVOV\n"
               "lGAxxbjaOxXB5q6AAifcdhZD0YvzxmI0RxTeJ1QS7JwMbifow5rm+kVGcKSF2yOt\n"
               "vy9/XYDmnCq9ZtVJ1u/meXLP\n"
               "-----END PRIVATE KEY-----\n")
    
    return {
        "type": "service_account",
        "project_id": "inventory-database-484717",
        "private_key_id": "571920803e7634af6a9979d9b50bb75fcf845861",
        "private_key": raw_key,
        "client_email": "inventory@inventory-database-484717.iam.gserviceaccount.com",
        "client_id": "100700200416747731347",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/inventory%40inventory-database-484717.iam.gserviceaccount.com"
    }

try:
    creds = get_creds()
    spread = Spread('Inventory_Database', config=creds)
    
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
