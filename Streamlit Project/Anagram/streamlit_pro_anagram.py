import streamlit as st

def CheckAnagram(str1, str2):
    if sorted(str1) == sorted(str2):
        return "Anagram"
    else:
        return "Not Anagram"

def validateAnagram():
    str1 = st.session_state.string1.lower()
    str2 = st.session_state.string2.lower()
    result = CheckAnagram(str1, str2)
    
    if result == "Anagram":
        st.session_state.result_color = "green"
        st.session_state.result_text = result
    else:
        st.session_state.result_color = "red"
        st.session_state.result_text = result


st.set_page_config(page_title="Anagram Checker", layout="centered", initial_sidebar_state="collapsed")

st.title("Anagram Checker")


st.text_input("Enter the first string:", key="string1")
st.text_input("Enter the second string:", key="string2")

if st.button("Check for Anagram"):
    validateAnagram()

if 'result_text' in st.session_state:
    st.markdown(f"<h2 style='color: {st.session_state.result_color};'>{st.session_state.result_text}</h2>", unsafe_allow_html=True)