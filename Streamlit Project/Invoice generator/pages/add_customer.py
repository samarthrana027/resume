import streamlit as st
import pandas as pd

customers_df = pd.read_csv("customers.csv")
st.title("Add New Customer")
st.write("Please fill out the form below to add a new customer.")
customer_name = st.text_input("Customer Name")
customer_address=st.text_area("Customers Address")
customer_email = st.text_input("Customer Email")
customer_phone = st.text_input("Customer Phone Number")
if st.button("Add Customer"):
    if customer_name and customer_email and customer_phone:
        new_customer = pd.DataFrame({
            "Name": [customer_name],
            "Address":customer_address,
            "Phone": [customer_phone],
            "Email": [customer_email]
        })
        
        customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
        
        
        customers_df.to_csv("../customers.csv", index=False)
        
        
        st.success("Customer added successfully!")
        
        
        st.write(customers_df)
    else:
        st.error("Please fill in all fields before submitting.")