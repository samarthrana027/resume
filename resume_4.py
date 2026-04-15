import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Professional Resume UI",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Custom CSS to match resume style
# -----------------------------

st.markdown(
    """
    <style>
    .left-panel {
        background-color: #2F3E4E;
        color: white;
        padding: 20px;
        border-radius: 10px;
        height: 100%;
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
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Input Fields (Editable Resume)
# -----------------------------

st.title("Resume Builder — Professional Layout")

col_left, col_right = st.columns([1, 2])

with col_left:

    st.markdown('<div class="left-panel">', unsafe_allow_html=True)

    photo = st.file_uploader("Upload Profile Photo", type=["jpg", "png", "jpeg"])

    if photo:
        st.image(photo, width=150)

    st.markdown("### Contact")

    email = st.text_input("Email", "samarthrana148@gmail.com")
    phone = st.text_input("Phone", "+91 9726995988")
    address = st.text_input("Address", "Globcon Splendora, Pal")

    st.markdown("### Education")

    education1 = st.text_input(
        "Degree",
        "B.E. Computer Engineering — C.K. Pithawala College"
    )

    education2 = st.text_input(
        "12th",
        "Shri Swaminarayan Mission School"
    )

    education3 = st.text_input(
        "10th",
        "Shri Swaminarayan Mission School"
    )

    st.markdown("### Skills")

    skills = st.text_area(
        "Skills",
        "Designing & Graphics, Social media marketing, Product development lifecycle, Video Editing, Knowledge about Gemology"
    )

    st.markdown("### Languages")

    languages = st.text_area(
        "Languages",
        "English, Hindi, Gujarati"
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:

    st.markdown('<div class="right-panel">', unsafe_allow_html=True)

    name = st.text_input("Full Name", "Samarth Rana")

    title = st.text_input(
        "Professional Title",
        "Student at C.K. Pithawala College, Surat"
    )

    st.markdown('<div class="section-title">About Me</div>', unsafe_allow_html=True)

    about = st.text_area(
        "About",
        "As a student I am doing Computer Engineering at C.K. Pithawala College, Surat. I am learning new things and doing amazing projects and gaining knowledge about computer engineering."
    )

    st.markdown('<div class="section-title">Work Experience</div>', unsafe_allow_html=True)

    experience = st.text_area(
        "Experience",
        "Internships: Connected labs working on coding, testing, or hardware tasks. Services to small businesses. Teaching at tuition classes."
    )

    st.markdown('<div class="section-title">Training & Certifications</div>', unsafe_allow_html=True)

    training = st.text_area(
        "Training",
        "AI and ML Basics — Infosys Platform. Natural Programming Language. Workshop on AI and ML Booming in Market."
    )

    st.markdown('<div class="section-title">Hobbies</div>', unsafe_allow_html=True)

    hobbies = st.text_area(
        "Hobbies",
        "Reading, Playing Cricket, Travelling, Video Editing, Exploring new places"
    )

    st.markdown('<div class="section-title">Awards</div>', unsafe_allow_html=True)

    awards = st.text_area(
        "Awards",
        "3rd Rank in Essay Competition held by ONGC, Surat. 3rd Rank in Techfest Bidding Wars."
    )

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Preview Button
# -----------------------------

st.markdown("---")

if st.button("Generate Resume Preview", use_container_width=True):

    st.success("Resume Layout Generated Successfully")

    preview_left, preview_right = st.columns([1, 2])

    with preview_left:
        if photo:
            st.image(photo, width=150)

        st.markdown("### Contact")
        st.write(email)
        st.write(phone)
        st.write(address)

        st.markdown("### Skills")
        st.write(skills)

        st.markdown("### Languages")
        st.write(languages)

    with preview_right:
        st.header(name)
        st.write(title)

        st.markdown("### About Me")
        st.write(about)

        st.markdown("### Work Experience")
        st.write(experience)

        st.markdown("### Training & Certifications")
        st.write(training)

        st.markdown("### Hobbies")
        st.write(hobbies)

        st.markdown("### Awards")
        st.write(awards)
