import streamlit as st
import pandas as pd
from db_utils import (
    initialize_database, add_medicine, view_medicines, search_medicine,
    update_stock, check_expiry, check_low_stock
)

# Initialize DB on app start
initialize_database()

st.set_page_config(page_title="🏥 Medical Inventory System", layout="wide")

st.title("🏥 Medical Inventory Management System")

menu = st.sidebar.selectbox(
    "Navigation Menu",
    ["Add Medicine", "View All Medicines", "Search Medicine", "Update Stock", "Check Expiry", "Check Low Stock"]
)

# Add Medicine
if menu == "Add Medicine":
    st.header("➕ Add New Medicine")
    name = st.text_input("Medicine Name")
    batch = st.text_input("Batch No.")
    expiry = st.date_input("Expiry Date")
    qty = st.number_input("Quantity", min_value=0)
    price = st.number_input("Price (₹)", min_value=0.0, step=0.1)
    supplier = st.text_input("Supplier")

    if st.button("Add Medicine"):
        if name and batch:
            add_medicine(name, batch, expiry, qty, price, supplier)
            st.success(f"✅ '{name}' added successfully!")
        else:
            st.warning("Please fill all required fields.")

# View All Medicines
elif menu == "View All Medicines":
    st.header("📋 All Medicines")
    data = view_medicines()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Name", "Batch No", "Expiry Date", "Quantity", "Price", "Supplier"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No medicines found in database.")

# Search Medicine
elif menu == "Search Medicine":
    st.header("🔍 Search Medicine")
    keyword = st.text_input("Enter medicine name or batch number:")
    if st.button("Search"):
        results = search_medicine(keyword)
        if results:
            df = pd.DataFrame(results, columns=["ID", "Name", "Batch No", "Expiry Date", "Quantity", "Price", "Supplier"])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No results found.")

# Update Stock
elif menu == "Update Stock":
    st.header("📦 Update Medicine Stock")
    med_id = st.number_input("Enter Medicine ID", min_value=1)
    qty_change = st.number_input("Enter quantity change (+ to add, - to remove)", step=1)
    if st.button("Update Stock"):
        update_stock(med_id, qty_change)
        st.success("✅ Stock updated successfully!")

# Check Expiry
elif menu == "Check Expiry":
    st.header("⚠️ Expired Medicines")
    expired = check_expiry()
    if expired:
        df = pd.DataFrame(expired, columns=["ID", "Name", "Batch No", "Expiry Date", "Quantity", "Price", "Supplier"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No expired medicines found.")

# Check Low Stock
elif menu == "Check Low Stock":
    st.header("📉 Low Stock Alert")
    threshold = st.number_input("Stock Threshold", min_value=1, value=10)
    if st.button("Check"):
        low_stock = check_low_stock(threshold)
        if low_stock:
            df = pd.DataFrame(low_stock, columns=["ID", "Name", "Batch No", "Expiry Date", "Quantity", "Price", "Supplier"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("All medicines have sufficient stock.")
