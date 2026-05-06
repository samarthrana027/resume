import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

customers=pd.read_csv("customers.csv")
products=pd.read_csv("products.csv")

main_page=st.Page(
    page="main.py",
    title="Main Page",
    icon="🏠",
    default=True
)

add_customer=st.Page(
    page="pages/add_customer.py",
    title="Add Customer",
    icon="👤"
)
generate_invoice=st.Page(
    page="pages/generate_invoice.py",
    title="generate invoice",
    icon="🧾"
)


pg=st.navigation(
    {   
        "main":[main_page],
        "customer":[add_customer],
        "Invoice":[generate_invoice],
    }
)




pg.run()