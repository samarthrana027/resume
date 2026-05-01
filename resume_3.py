import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Unique Resume Builder",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 20px;
    }
    .section {
        background-color: #F4F6F7;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .footer {
        text-align: center;
        color: gray;
        font-size: 14px;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Session State
# -----------------------------

if "education_list" not in st.session_state:
    st.session_state.education_list = []

# -----------------------------
# Title
# -----------------------------

st.markdown('<div class="main-title">📄 Smart Resume Builder</div>', unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("⚙️ Settings")

template = st.sidebar.selectbox(
    "Select Resume Template",
    ["Classic", "Modern", "Simple"]
)

st.sidebar.info(
    "Fill all sections to generate your professional resume preview."
)

# -----------------------------
# Layout Columns
# -----------------------------

col1, col2 = st.columns(2)

# -----------------------------
# Left Column
# -----------------------------

with col1:

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.header("👤 Personal Information")

    photo = st.file_uploader(
        "Upload Profile Photo",
        type=["jpg", "png", "jpeg"]
    )

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.header("🎓 Education")

    edu_input = st.text_input("Enter Education Detail")

    if st.button("Add Education"):
        if edu_input:
            st.session_state.education_list.append(edu_input)

    for i, edu in enumerate(st.session_state.education_list):
        st.write(f"{i+1}. {edu}")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Right Column
# -----------------------------

with col2:

    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.header("🧠 Skills")
    skills = st.text_area("Enter your Skills")

    st.header("💼 Experience")
    experience = st.text_area("Enter your Experience")

    st.header("🚀 Projects")
    projects = st.text_area("Enter your Projects")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Preview Button
# -----------------------------

st.markdown("---")

if st.button("📄 Preview Resume", use_container_width=True):

    st.success("Resume Preview Generated")

    preview_col1, preview_col2 = st.columns([1, 3])

    with preview_col1:
        if photo:
            st.image(photo, width=150)

    with preview_col2:
        st.subheader(name)
        st.write("📧", email)
        st.write("📞", phone)
        st.write("📍", address)

    st.markdown("### 🎓 Education")

    for edu in st.session_state.education_list:
        st.write("•", edu)

    st.markdown("### 🧠 Skills")
    st.write(skills)

    st.markdown("### 💼 Experience")
    st.write(experience)

    st.markdown("### 🚀 Projects")
    st.write(projects)

# -----------------------------
# Footer
# -----------------------------

st.markdown(
    '<div class="footer">Built with Streamlit | Resume Builder Project</div>',
    unsafe_allow_html=True
)
