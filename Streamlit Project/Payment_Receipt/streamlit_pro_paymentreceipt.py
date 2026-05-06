import streamlit as st

class PaymentReceipt:
    def __init__(self, customer_name, amount, payment_method):
        self.customer_name = customer_name
        self.amount = amount
        self.payment_method = payment_method

    def generate_receipt(self):
        receipt = f"""
        Payment Receipt
        -----------------
        Customer Name: {self.customer_name}
        Amount: {self.amount:.2f}
        Payment Method: {self.payment_method}
        -----------------
        Thank you for your payment!
        """
        return receipt

def main():
    st.title("Payment Receipt Generator")
    
    customer_name = st.text_input("Enter customer name:")
    amount = st.number_input("Enter payment amount:", min_value=0.0, format="%.2f")
    payment_method = st.selectbox("Select payment method:", ["Credit Card", "Debit Card", "PayPal", "Cash"])

    if st.button("Generate Receipt"):
        receipt = PaymentReceipt(customer_name, amount, payment_method)
        st.text(receipt.generate_receipt())

if __name__ == "__main__":
    main()