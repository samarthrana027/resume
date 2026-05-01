import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd

# Download required NLTK data (only first time)
nltk.download('punkt')
nltk.download('stopwords')

# Title
st.title("Stop Word Analysis using Streamlit and NLP")

st.write("Enter text below to analyze stop words and remaining keywords.")

# Text input
text_input = st.text_area("Enter your text here:")

if st.button("Analyze"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Tokenize text
        words = word_tokenize(text_input.lower())

        # Get English stop words
        stop_words = set(stopwords.words('english'))

        # Separate stop words and filtered words
        stopword_list = [word for word in words if word in stop_words]
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

        # Count frequencies
        stopword_freq = Counter(stopword_list)
        filtered_freq = Counter(filtered_words)

        # Display results
        st.subheader("Total Words")
        st.write(len(words))

        st.subheader("Stop Words Found")
        st.write(len(stopword_list))
        st.write(stopword_list)

        st.subheader("Filtered Words (Without Stop Words)")
        st.write(len(filtered_words))
        st.write(filtered_words)

        # Display frequency tables
        st.subheader("Stop Word Frequency")
        if stopword_freq:
            df_stop = pd.DataFrame(stopword_freq.items(), columns=["Stop Word", "Frequency"])
            st.dataframe(df_stop)
        else:
            st.write("No stop words found.")

        st.subheader("Keyword Frequency (Without Stop Words)")
        if filtered_freq:
            df_filtered = pd.DataFrame(filtered_freq.items(), columns=["Word", "Frequency"])
            st.dataframe(df_filtered)
        else:
            st.write("No keywords found.")
