# app.py - Minimal working version (blank page fix ke liye)

import streamlit as st
import io
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Page config pehle daalo
st.set_page_config(page_title="Resume Builder - Test", layout="wide")

# Debug message sabse upar (terminal aur app mein dikhega)
st.write("App starting... Hello Awais! Yeh line dikhi to UI chal raha hai.")

st.title("📄 Simple Resume Builder (Test Version)")

st.markdown("**Yeh minimal version hai – agar yeh title aur inputs dikhte hain to baqi code mein masla tha.**")

# Sidebar for info
with st.sidebar:
    st.header("Status")
    st.info("No API calls in this version → no crash")
    st.write("Streamlit version check:", st.__version__)

# Main inputs
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Your Details")
    name = st.text_input("Full Name", "Awais Khan")
    job = st.text_input("Job Title", "AI Enthusiast / Developer")
    email = st.text_input("Email", "awais@example.com")
    phone = st.text_input("Phone", "+92-300-1234567")
    location = st.text_input("Location", "Islamabad, Pakistan")

    summary = st.text_area("About Me", "Passionate about building tools...", height=120)
    education = st.text_area("Education", "BS Computer Science - Some University, 2020-2024", height=100)
    experience = st.text_area("Experience", "Freelance AI projects...", height=150)
    skills = st.text_area("Skills", "Python, Streamlit, Groq, HuggingFace", height=100)

    if st.button("Generate Preview"):
        st.success("Preview generating...")

with col2:
    st.subheader("Resume Preview")
    st.markdown(f"## {name.upper()}")
    st.markdown(f"**{job}**")
    st.markdown(f"{phone} | {email} | {location}")
    
    st.markdown("### ABOUT ME")
    st.write(summary)
    
    st.markdown("### EDUCATION")
    st.write(education)
    
    st.markdown("### EXPERIENCE")
    st.write(experience)
    
    st.markdown("### SKILLS")
    st.write(skills)

# Simple DOCX download (no PDF to avoid fpdf2 issue abhi)
def create_simple_docx():
    doc = Document()
    p = doc.add_paragraph(name.upper())
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.runs[0]
    run.font.size = Pt(24)
    run.bold = True
    
    doc.add_paragraph(job).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"{phone} | {email} | {location}").alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_heading("ABOUT ME", level=1)
    doc.add_paragraph(summary)
    
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

if st.button("Download Simple DOCX"):
    docx_file = create_simple_docx()
    st.download_button(
        label="📥 Download Resume.docx",
        data=docx_file,
        file_name=f"{name}_Resume.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.markdown("---")
st.caption("Agar yeh page poori dikhi (title, inputs, preview) to bata – ab hum Groq/HF wapis add karenge step by step.")
