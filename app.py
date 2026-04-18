import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("churn_model.pkl")

# Page config
st.set_page_config(page_title="Customer Churn Predictor", layout="centered")

# -------- CUSTOM CSS -------- #
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    .main {
        background-color: white;
    }
    h1 {
        color: #2E86C1;
        text-align: center;
    }
    .box {
        padding: 15px;
        border-radius: 10px;
        background-color: #F4F6F7;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------- HEADER -------- #
st.markdown("<h1>📊 Customer Churn Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Predict whether a customer will leave the service</p>", unsafe_allow_html=True)

st.markdown("---")

# -------- CUSTOMER INFO -------- #
st.markdown("<div class='box'><b>👤 Customer Information</b></div>", unsafe_allow_html=True)

gender = st.selectbox("Gender", ["Male", "Female"])
senior = st.selectbox("Senior Citizen", [0, 1])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])

tenure = st.slider("Tenure (Months)", 0, 72, 12)

# -------- SERVICES -------- #
st.markdown("<div class='box'><b>📡 Services</b></div>", unsafe_allow_html=True)

phone = st.selectbox("Phone Service", ["Yes", "No"])
multiple = st.selectbox("Multiple Lines", ["Yes", "No"])

internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

online_sec = st.selectbox("Online Security", ["Yes", "No"])
online_backup = st.selectbox("Online Backup", ["Yes", "No"])
device_prot = st.selectbox("Device Protection", ["Yes", "No"])
tech_support = st.selectbox("Tech Support", ["Yes", "No"])

stream_tv = st.selectbox("Streaming TV", ["Yes", "No"])
stream_movies = st.selectbox("Streaming Movies", ["Yes", "No"])

# -------- BILLING -------- #
st.markdown("<div class='box'><b>💳 Billing Information</b></div>", unsafe_allow_html=True)

paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
monthly = st.number_input("Monthly Charges", 0, 200, 50)
total = st.number_input("Total Charges", 0, 10000, 500)

contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

payment = st.selectbox("Payment Method", [
    "Bank transfer (automatic)",
    "Credit card (automatic)",
    "Electronic check",
    "Mailed check"
])

st.markdown("---")

# -------- ENCODING -------- #
def yes_no(val):
    return 1 if val == "Yes" else 0

gender = 1 if gender == "Female" else 0

partner = yes_no(partner)
dependents = yes_no(dependents)
phone = yes_no(phone)
multiple = yes_no(multiple)
online_sec = yes_no(online_sec)
online_backup = yes_no(online_backup)
device_prot = yes_no(device_prot)
tech_support = yes_no(tech_support)
stream_tv = yes_no(stream_tv)
stream_movies = yes_no(stream_movies)
paperless = yes_no(paperless)

# Internet encoding
dsl = 1 if internet == "DSL" else 0
fiber = 1 if internet == "Fiber optic" else 0
no_internet = 1 if internet == "No" else 0

# Contract encoding
month = 1 if contract == "Month-to-month" else 0
one_year = 1 if contract == "One year" else 0
two_year = 1 if contract == "Two year" else 0

# Payment encoding
bank = 1 if payment == "Bank transfer (automatic)" else 0
credit = 1 if payment == "Credit card (automatic)" else 0
electronic = 1 if payment == "Electronic check" else 0
mailed = 1 if payment == "Mailed check" else 0

# -------- PREDICTION -------- #
if st.button("🚀 Predict Churn"):

    input_data = np.array([[
        gender, senior, partner, dependents, tenure,
        phone, multiple, online_sec, online_backup,
        device_prot, tech_support, stream_tv, stream_movies,
        paperless, monthly, total,
        dsl, fiber, no_internet,
        month, one_year, two_year,
        bank, credit, electronic, mailed
    ]])

    prediction = model.predict(input_data)[0]

    st.markdown("### 🔍 Prediction Result")

    if prediction == 1:
        st.error("⚠️ Customer is likely to CHURN")
    else:
        st.success("✅ Customer will STAY")
