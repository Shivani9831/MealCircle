import firebase_admin
from firebase_admin import credentials, db
import datetime

# Initialize Firebase
cred = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mealcircle-default-rtdb.asia-southeast1.firebasedatabase.app/donations/-Ode6OJzuTQvUBdEtm0e'
})

# Sample donations data
sample_donations = {
    "donation_001": {
        "donor_name": "Green Restaurant",
        "donor_email": "contact@greenrestaurant.com",
        "donor_phone": "9876543210",
        "organization": "Green Restaurant",
        "food_type": "Cooked Meals",
        "quantity": "25 meals",
        "address": "123 Main Street, Bandra West",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400050",
        "special_instructions": "Available after 8 PM, please call before coming",
        "status": "available",
        "timestamp": datetime.datetime.now().isoformat()
    },
    "donation_002": {
        "donor_name": "Community Kitchen",
        "donor_email": "info@communitykitchen.org",
        "donor_phone": "9876543211",
        "organization": "Community Kitchen NGO",
        "food_type": "Fresh Produce",
        "quantity": "15 kg vegetables",
        "address": "456 Park Road, Connaught Place",
        "city": "Delhi",
        "state": "Delhi",
        "pincode": "110001",
        "special_instructions": "Fresh vegetables from today's market",
        "status": "available",
        "timestamp": datetime.datetime.now().isoformat()
    },
    "donation_003": {
        "donor_name": "Rahul Sharma",
        "donor_email": "rahul.sharma@email.com",
        "donor_phone": "9876543212",
        "organization": "",
        "food_type": "Packaged Food",
        "quantity": "20 packets of biscuits",
        "address": "789 Lake View Apartments, Koramangala",
        "city": "Bangalore",
        "state": "Karnataka",
        "pincode": "560034",
        "special_instructions": "Sealed packages, best before 6 months",
        "status": "available",
        "timestamp": datetime.datetime.now().isoformat()
    },
    "donation_004": {
        "donor_name": "Sweet Bakes",
        "donor_email": "orders@sweetbakes.com",
        "donor_phone": "9876543213",
        "organization": "Sweet Bakes Bakery",
        "food_type": "Bakery Items",
        "quantity": "30 bread loaves + 50 pastries",
        "address": "321 Baker Street, Punjabi Bagh",
        "city": "Delhi",
        "state": "Delhi",
        "pincode": "110026",
        "special_instructions": "Today's fresh bake, collect before 6 PM",
        "status": "claimed",
        "timestamp": datetime.datetime.now().isoformat()
    }
}

# Add to Firebase
ref = db.reference('donations')
for donation_id, donation_data in sample_donations.items():
    ref.child(donation_id).set(donation_data)

print("✅ Sample data added successfully!")
print("🎯 Now run: streamlit run app.py")