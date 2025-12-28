import streamlit as st
import os
from groq import Groq

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="ResumeForge AI",
    page_icon="📄",
    layout="wide",
)

# =============================
# GROQ CLIENT
# =============================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =============================
# PREMIUM CSS (SAAS UI)
# =============================
st.markdown("""
<style>
body {
    background-color: #0b0f19;
}
.hero-title {
    font-size: 56px;
    font-weight: 900;
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 22px;
    color: #c7d2fe;
}
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 0 40px rgba(99,102,241,0.15);
}
.label {
    font-weight: 600;
    color: #e5e7eb;
}
.resume-preview {
    background: #020617;
    color: #e5e7eb;
    padding: 28px;
    border-radius: 16px;
    height: 650px;
    overflow-y: auto;
    font-size: 15px;
    line-height: 1.7;
    border-left: 4px solid #6366f1;
}
button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #06b6d4);
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HERO SECTION
# =============================
st.markdown("<div class='hero-title'>ResumeForge AI</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>Build recruiter-ready resumes powered by AI</div>", unsafe_allow_html=True)
st.write("Trusted-quality resume generation for engineers, students & professionals.")

st.markdown("---")

# =============================
# MAIN LAYOUT
# =============================
left, right = st.columns([1, 1.2])

# =============================
# INPUT PANEL
# =============================
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧑 Candidate Information")

    name = st.text_input("Full Name")
    role = st.selectbox(
        "Target Role",
        ["AI Full Stack Developer", "Software Engineer", "Data Scientist", "Web Developer"]
    )
    education = st.text_area("Education", height=80)
    skills = st.text_area("Technical Skills (comma separated)", height=80)
    projects = st.text_area("Projects (with impact)", height=100)
    experience = st.text_area("Experience (optional)", height=80)

    generate = st.button("✨ Generate Resume", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =============================
# RESUME PREVIEW
# =============================
with right:
    st.subheader("📄 Live Resume Preview")

    if generate:
        if not name or not skills or not education:
            st.warning("Please complete all required fields.")
        else:
            with st.spinner("Crafting a premium resume..."):
                prompt = f"""
Create a premium, ATS-friendly resume.

Candidate Name: {name}
Target Role: {role}
Education: {education}
Skills: {skills}
Projects: {projects}
Experience: {experience}

Guidelines:
- Use strong action verbs
- Quantify impact where possible
- Professional corporate tone
- Clear sections and bullet points
- Suitable for top tech companies
"""

                try:
                    response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "system", "content": "You are a senior resume writer at a tech hiring firm."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.25,
                        max_tokens=900
                    )

                    resume = response.choices[0].message.content

                    st.markdown(
                        f"<div class='resume-preview'><pre>{resume}</pre></div>",
                        unsafe_allow_html=True
                    )

                    st.download_button(
                        "⬇ Download Resume",
                        resume,
                        file_name=f"{name.replace(' ', '_')}_Resume.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                except Exception:
                    st.error("AI generation failed. Please retry.")

    else:
        st.info("Fill details and click **Generate Resume** to preview.")

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("ResumeForge AI · Built like a real product · Powered by AI")
