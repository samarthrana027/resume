import streamlit as st

# Title of the app
st.title("My Resume Builder")

st.header("Personal Information")

# User Inputs
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
address = st.text_area("Address")

st.header("Education")
education = st.text_area("Enter your Education Details")

st.header("Skills")
skills = st.text_area("Enter your Skills")

st.header("Experience")
experience = st.text_area("Enter your Experience")

st.header("Projects")
projects = st.text_area("Enter your Projects")

# Generate Resume Button
if st.button("Generate Resume"):

    st.success("Resume Generated Successfully!")

    st.subheader("Your Resume")

    st.write("### Personal Information")
    st.write("Name:", name)
    st.write("Email:", email)
    st.write("Phone:", phone)
    st.write("Address:", address)

    st.write("### Education")
    st.write(education)

    st.write("### Skills")
    st.write(skills)

    st.write("### Experience")
    st.write(experience)

    st.write("### Projects")
    st.write(projects)