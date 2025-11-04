#!/usr/bin/env python3
"""
Ultra Simple Construction Estimation App
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Construction Estimation System",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Construction Estimation System")
st.subheader("Ultra Simple Version")

st.write("Welcome to the Construction Estimation System!")

# Initialize session state
if 'measurements' not in st.session_state:
    st.session_state.measurements = pd.DataFrame(columns=['Item', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount'])

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Dashboard", "Add Item", "View Items"])

if page == "Dashboard":
    st.header("Dashboard")
    st.metric("Total Items", len(st.session_state.measurements))
    if not st.session_state.measurements.empty:
        st.metric("Total Cost", f"₹{st.session_state.measurements['Amount'].sum():,.2f}")
    
elif page == "Add Item":
    st.header("Add New Item")
    with st.form("add_item_form"):
        item = st.text_input("Item Number")
        description = st.text_input("Description")
        unit = st.selectbox("Unit", ["Cum", "Sqm", "Nos", "Kg", "Ltr"])
        quantity = st.number_input("Quantity", min_value=0.0, value=1.0)
        rate = st.number_input("Rate", min_value=0.0, value=0.0)
        
        submitted = st.form_submit_button("Add Item")
        if submitted:
            amount = quantity * rate
            new_item = pd.DataFrame({
                'Item': [item],
                'Description': [description],
                'Unit': [unit],
                'Quantity': [quantity],
                'Rate': [rate],
                'Amount': [amount]
            })
            st.session_state.measurements = pd.concat([st.session_state.measurements, new_item], ignore_index=True)
            st.success("Item added successfully!")

elif page == "View Items":
    st.header("All Items")
    if st.session_state.measurements.empty:
        st.info("No items added yet.")
    else:
        st.dataframe(st.session_state.measurements, use_container_width=True)
        st.metric("Total Cost", f"₹{st.session_state.measurements['Amount'].sum():,.2f}")