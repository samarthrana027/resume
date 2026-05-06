import streamlit as st
import pandas as pd

invoice_df = pd.read_csv("products.csv")
st.title("Add New ID")
st.write("Please fill out the form below to add a new ID")
product_id = st.text_input("Product ID")
product_name=st.text_input("Product Name")
product_description = st.text_input("Product Description")
product_price = st.text_input("Product Price")
if st.button("Add Product"):
    if product_name and product_description and product_price:
        new_product = pd.DataFrame({
            "ID": [product_id],
            "Name": [product_name],
            "Description": [product_description],
            "Price": [product_price]
        })
        
        invoice_df = pd.concat([invoice_df, new_product], ignore_index=True)
        
        
        invoice_df.to_csv("../products.csv", index=False)
        
        
        st.success("Product added successfully!")
        
        
        st.write(invoice_df)
    else:
        st.error("Please fill in all fields before submitting.")