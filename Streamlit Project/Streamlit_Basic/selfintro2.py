import streamlit as st
def submit_function():
    st.markdown("DATA HAS SUBMITTED ")
with st.form(key="login_form"):
    st.title("Login form")
    Name=st.text_input(label="Name",placeholder="Enter your Full Name: ")
    mobile_number=st.text_input(label="Phone Number",placeholder="Enter the Phone number:")
    Email=st.text_input(label="Email",placeholder="Enter your email: ")
    department=st.text_input(label="Department",placeholder="Enter your Department:")
    Id=st.text_input(label="Enrollment No.",placeholder="Enter your Enrollment No.:")
    dob=st.date_input(label="Date of birth")
    Username=st.text_input(label="Username",placeholder="Enter your username: ")
    col1,col2=st.columns(2,gap="medium")
    Password=col1.text_input(label="Password",placeholder="Enter your passwsord",type="password")
    confirm_password=col2.text_input(label="Confirm Password",placeholder="Confirm Password",type="password")
    gender=st.radio(label="Gender",options=['Male','Female','Other'])
    submit=st.form_submit_button(label="Submit form",type="secondary",use_container_width=True)
    if submit:
        submit_function()
