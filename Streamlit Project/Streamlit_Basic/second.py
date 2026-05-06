import streamlit as st
def submit_function():
    st.markdown("DATA SUBMITTED SUCCESFULLY")
with st.form(key="login_form"):
    st.title("Login form")
    name=st.text_input(label="Name",placeholder="Enter your name: ")
    Email=st.text_input(label="Email",placeholder="Enter your email: ")
    dob=st.date_input(label="Date of birth")
    Username=st.text_input(label="Username",placeholder="Enter your username: ")
    col1,col2=st.columns(2,gap="medium")
    Password=col1.text_input(label="Password",placeholder="Enter your passwsord",type="password")
    confirm_password=col2.text_input(label="Confirm Password",placeholder="Confirm Password",type="password")
    gender=st.radio(label="Gender",options=['Male','Female','Other'])
    hobbies=st.multiselect(label="Hobbies",options=['Football','Cricket','Volleyball'])
    submit=st.form_submit_button(label="Submit form",type="secondary",use_container_width=True)
    if submit:
        submit_function()

c1,c2=st.columns(2,gap='large')
c1.button(label="click me",use_container_width=True)
c2.link_button(label="Instagram",use_container_width=True,url="https://www.instagram.com/")