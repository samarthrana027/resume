import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Professional Resume",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>
.left-panel {
    background-color: #2F3E4E;
    color: white;
    padding: 20px;
    border-radius: 10px;
}
.right-panel {
    background-color: #F7F7F7;
    padding: 20px;
    border-radius: 10px;
}
.section-title {
    font-size: 20px;
    font-weight: bold;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------

st.title("My Resume")

# -----------------------------
# Layout
# -----------------------------

col_left, col_right = st.columns([1, 2])

# -----------------------------
# LEFT PANEL
# -----------------------------

with col_left:

    st.markdown('<div class="left-panel">', unsafe_allow_html=True)

    st.image(
        "sam photo.jpg",  # put your image file in same folder
        width=150
    )

    st.markdown("## Contact")

    st.write("Email: samarthrana148@gmail.com")
    st.write("Phone: +91 9726995988")
    st.write("Address: Globcon Splendora, Pal")

    st.markdown("## Education")

    st.write("B.E. Computer Engineering")
    st.write("C.K. Pithawala College")
    st.write("2024–2025 (Present)")

    st.write("12th Completed")
    st.write("Shri Swaminarayan Mission School")
    st.write("2023–2024")

    st.write("10th Completed")
    st.write("Shri Swaminarayan Mission School")
    st.write("2021–2022")

    st.markdown("## Skills")

    st.write("Designing & Graphics")
    st.write("Social Media Marketing")
    st.write("Product Development Lifecycle")
    st.write("Video Editing")
    st.write("Knowledge about Gemology")

    st.markdown("## Languages")

    st.write("English")
    st.write("Hindi")
    st.write("Gujarati")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RIGHT PANEL
# -----------------------------

with col_right:

    st.markdown('<div class="right-panel">', unsafe_allow_html=True)

    st.header("Samarth Rana")

    st.write("Student at C.K. Pithawala College, Surat")

    st.markdown("## About Me")

    st.write(
        "As a student I am doing Computer Engineering at C.K. "
        "Pithawala College, Surat. I am learning new things and "
        "doing amazing projects and gaining knowledge about "
        "computer engineering."
    )

    st.markdown("## Work Experience")

    st.write("Internships (2024–2025 Present)")
    st.write("• Connected labs working on coding, testing, or hardware tasks")
    st.write("• Services to small businesses")
    st.write("• Teaching at tuition classes")

    st.markdown("## Training & Certifications")

    st.write("AI and ML Basics — Infosys Platform")
    st.write("Natural Programming Language")
    st.write("Workshop on AI and ML Booming in Market")

    st.markdown("## Hobbies")

    st.write("Reading")
    st.write("Playing Cricket")
    st.write("Travelling")
    st.write("Video Editing")
    st.write("Exploring new places")

    st.markdown("## Awards")

    st.write("3rd Rank in Essay Competition held by ONGC, Surat")
    st.write("3rd Rank in Techfest Bidding Wars")

    st.markdown('</div>', unsafe_allow_html=True)