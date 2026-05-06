import streamlit as st
st.title("This is a title",anchor=False)
st.header(":violet[This is a header]",anchor=False,divider="violet")
st.subheader(":orange[This is a sub header]",anchor=False,divider="orange")
st.text("This is a text")
st.html("<H1>This is a H1 tag</H1>")
col1,col2=st.columns(2,gap='large')
with col1:
    st.html("<H2>SAMARTH</H2>")
with col2:
    st.html("<H2>RANA</H2>")
st.title("This is a second title")

