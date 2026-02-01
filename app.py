import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# ================= FIREBASE SETUP =================
firebase_enabled = False

try:
    import firebase_admin
    from firebase_admin import credentials, db

    if not firebase_admin._apps:
        firebase_creds = dict(st.secrets["FIREBASE"])
        firebase_creds["private_key"] = firebase_creds["private_key"].replace("\\n", "\n")

        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred, {
            "databaseURL": firebase_creds["databaseURL"]
        })

    firebase_enabled = True
    st.success("🔥 Firebase Connected Successfully!")

except Exception as e:
    st.error("❌ Firebase Connection Failed")
    st.error(str(e))

# ================= IMAGE FUNCTION =================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return ""

# ================= LOAD IMAGES =================
background_b64 = get_base64_image("assets/background.jpg")
logo_b64 = get_base64_image("assets/logo.png")

# ================= PAGE CONFIG =================
st.set_page_config(page_title="MealCircle", page_icon="🍽", layout="wide")

# ================= CSS =================
st.markdown(f"""
<style>
.stApp {{
    background-image: url('data:image/jpg;base64,{background_b64}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.main .block-container {{
    background-color: rgba(255,255,255,0.9);
    padding: 2rem;
    border-radius: 15px;
}}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR LOGO =================
st.sidebar.markdown(f"""
<div style="text-align:center;">
<img src="data:image/png;base64,{logo_b64}" width="150">
</div>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("🍽 MealCircle - From Leftovers to Lifesavers")
st.write("Where Kindness is always on the Menu!")

# ================= NAVIGATION =================
page = st.sidebar.radio("Go to", ["Home", "Donate Food", "View Donations", "Analytics"])

# ================= HOME =================
if page == "Home":
    st.header("Welcome to MealCircle!")
    st.write("Donate extra food and help reduce hunger ❤️")

# ================= DONATE =================
elif page == "Donate Food":
    st.header("🎁 Donate Food")

    with st.form("donation_form"):
        name = st.text_input("Your Name")
        phone = st.text_input("Phone")
        food_type = st.selectbox("Food Type", ["Cooked Meals", "Fresh Fruits", "Packaged Food"])
        quantity = st.text_input("Quantity")
        city = st.text_input("City")
        address = st.text_area("Pickup Address")
        submit = st.form_submit_button("Submit")

    if submit:
        if name and phone and quantity and city:
            data = {
                "name": name,
                "phone": phone,
                "food_type": food_type,
                "quantity": quantity,
                "city": city,
                "address": address,
                "time": datetime.now().isoformat(),
                "status": "available"
            }

            if firebase_enabled:
                db.reference("donations").push(data)
                st.success("Donation saved to Firebase ✅")
            else:
                st.error("Firebase not connected ❌")

# ================= VIEW DONATIONS =================
elif page == "View Donations":
    st.header("📋 Donations List")

    if firebase_enabled:
        donations = db.reference("donations").get()
    else:
        donations = None

    if donations:
        for k, v in donations.items():
            st.write(v)
    else:
        st.info("No donations yet")

# ================= ANALYTICS =================
elif page == "Analytics":
    st.header("📊 Analytics")

    if firebase_enabled:
        donations = db.reference("donations").get() or {}
        st.metric("Total Donations", len(donations))
    else:
        st.info("Firebase not connected")

# ================= FIREBASE TEST BUTTON =================
if st.sidebar.button("Test Firebase"):
    if firebase_enabled:
        db.reference("test").set({"hello": "Shivani"})
        st.success("Firebase WRITE SUCCESS 🎉")
    else:
        st.error("Firebase NOT connected ❌")
