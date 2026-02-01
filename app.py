import streamlit as st


import pandas as pd
from datetime import datetime
import base64

# --- Firebase setup ---
try:
    import firebase_admin
    from firebase_admin import credentials, db

    if not firebase_admin._apps:
        # Load credentials from Streamlit Secrets
        firebase_creds = st.secrets["FIREBASE"]
        firebase_creds["private_key"] = firebase_creds["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred, {
            "databaseURL": firebase_creds["databaseURL"]
        })

   # --- Firebase setup ---
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


# --- Utility to encode images to base64 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return ""

# --- Encode images ---
background_b64 = get_base64_image("assets/background.jpg")
logo_b64 = get_base64_image("assets/logo.png")

# --- Page setup ---
st.set_page_config(page_title="MealCircle", page_icon="🍽", layout="wide")

# --- Custom CSS ---
st.markdown(f"""
<style>
.stApp {{
    background-image: url('data:image/jpg;base64,{background_b64}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.stMarkdown, .stText, .stTitle, .stHeader, h1,h2,h3,h4,h5,h6,p,div,span {{
    color: #1a1a1a !important;
}}
.stTextInput input, .stTextArea textarea, .stSelectbox select {{
    color: #1a1a1a !important;
    background-color: rgba(255, 255, 255, 0.9) !important;
}}
.main .block-container {{
    background-color: rgba(255, 255, 255, 0.92);
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem;
    border: 1px solid #e0e0e0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}}
.stMetric {{
    background-color: rgba(255, 255, 255, 0.9);
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}}
.logo-container {{
    text-align: center;
    margin-bottom: 1rem;
    padding: 1rem;
}}
.logo-img {{
    max-width: 180px;
    height: auto;
    border-radius: 10px;
}}
.stForm {{
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}}
.stButton button {{
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
}}
.stButton button:hover {{
    background-color: #45a049;
}}
</style>
""", unsafe_allow_html=True)

# --- Sidebar logo ---
st.sidebar.markdown(f"""
<div class="logo-container">
    <img src="data:image/png;base64,{logo_b64}" class="logo-img" alt="MealCircle Logo">
</div>
""", unsafe_allow_html=True)

# --- App title ---
st.title("🍽 MealCircle - From Leftovers to Lifesavers")
st.write("Where Kindness is always on the Menu!")

# --- Navigation ---
page = st.sidebar.radio("Go to", ["Home", "Donate Food", "View Donations", "Analytics"])

# --- HOME ---
if page == "Home":
    st.header("Welcome to MealCircle!")
    st.write("""
    How it works:
    - 🎁 Donate extra food from events/restaurants
    - 📋 Find donations near you
    - 🤝 Help reduce food waste
    """)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Meals Shared", "1,247")
    with col2:
        st.metric("Donors", "89")
    with col3:
        st.metric("Cities", "15")

# --- DONATE FOOD ---
elif page == "Donate Food":
    st.header("🎁 Donate Food")
    with st.form("donation_form"):
        name = st.text_input("Your Name")
        phone = st.text_input("Phone")
        food_type = st.selectbox("Food Type", ["Cooked Meals", "Fresh Fruits", "Packaged Food"])
        quantity = st.text_input("Quantity (e.g., 10 meals)")
        city = st.text_input("City")
        address = st.text_area("Pickup Address")
        submitted = st.form_submit_button("Submit Donation")

        if submitted:
            if name and phone and food_type and quantity and city:
                donation_data = {
                    "donor_name": name,
                    "donor_phone": phone,
                    "food_type": food_type,
                    "quantity": quantity,
                    "city": city,
                    "address": address,
                    "timestamp": datetime.now().isoformat(),
                    "status": "available"
                }
                if firebase_enabled:
                    try:
                        ref = db.reference("donations")
                        donation_id = ref.push().key
                        ref.child(donation_id).set(donation_data)
                        st.success("✅ Thank you! Your donation has been posted.")
                    except Exception as e:
                        st.error(f"Firebase Error: {str(e)}")
                else:
                    st.info("Firebase disabled. Donation not saved.")
            else:
                st.error("Please fill all required fields.")

# --- VIEW DONATIONS ---
elif page == "View Donations":
    st.header("📋 Available Donations")
    donations = {}
    if firebase_enabled:
        try:
            ref = db.reference("donations")
            donations = ref.get() or {}
        except:
            st.warning("Firebase disabled. Showing empty donations.")

    if not donations:
        st.info("No donations available right now.")
    else:
        for donation_id, donation in donations.items():
            if donation.get("status") == "available":
                st.write(f"**{donation.get('food_type','Food')}** - {donation.get('quantity','')}")
                st.write(f"📍 {donation.get('city','')} | 📞 {donation.get('donor_phone','')}")
                st.write(f"🏠 {donation.get('address','')}")
                if st.button(f"Claim This", key=donation_id):
                    if firebase_enabled:
                        ref.child(donation_id).update({"status": "claimed"})
                    st.success("Donation claimed! Contact the donor.")
                    st.rerun()
                st.markdown("---")

# --- ANALYTICS ---
elif page == "Analytics":
    st.header("📊 Analytics")
    donations = {}
    if firebase_enabled:
        try:
            ref = db.reference("donations")
            donations = ref.get() or {}
        except:
            st.warning("Firebase disabled. Showing empty analytics.")

    if donations:
        total_donations = len(donations)
        available_donations = sum(1 for d in donations.values() if d.get("status")=="available")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Donations", total_donations)
        with col2:
            st.metric("Available Now", available_donations)

        food_types = [d.get("food_type","Unknown") for d in donations.values()]
        food_counts = pd.Series(food_types).value_counts()
        st.bar_chart(food_counts)
    else:
        st.info("No data to show yet.")

st.sidebar.markdown("---")
st.sidebar.info("Made with ❤ for a hunger-free world")


if st.sidebar.button("Test Firebase"):
    if firebase_enabled:
        db.reference("test").set({"hello": "Shivani"})
        st.success("Firebase write success!")
    else:
        st.error("Firebase not connected")



