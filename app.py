import streamlit as st
import requests
import io
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ---------------- API ----------------

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets["HF_TOKEN"]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="AI Resume Architect", layout="wide")

# ---------------- AI CALL ----------------

def ask_ai(prompt):

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 500}}
        )

        data = response.json()

        if isinstance(data, list):
            return data[0]["generated_text"]

        return ""

    except:
        return ""

# ---------------- CLEAN TEXT ----------------

def clean(text):
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

# ---------------- GENERATE CV FROM PROMPT ----------------

def generate_from_prompt(user_prompt):

    prompt = f"""
Create a professional resume using this description.

User description:
{user_prompt}

Return format:

Name:
Title:
Email:
Phone:
Location:

Summary:
Education:
Experience:
Skills:
"""

    result = ask_ai(prompt)

    result = clean(result)

    return result

# ---------------- DOCX CREATOR ----------------

def create_docx(data):

    doc = Document()

    name = doc.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = name.add_run(data["name"].upper())
    run.bold = True
    run.font.size = Pt(24)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run(data["job"]).font.size = Pt(14)

    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.add_run(
        f'{data["phone"]} | {data["email"]} | {data["loc"]}'
    ).font.size = Pt(10)

    sections = [
        ("Summary", data["sum"]),
        ("Education", data["edu"]),
        ("Experience", data["exp"]),
        ("Skills", data["skills"])
    ]

    for title, content in sections:
        doc.add_heading(title.upper(), level=1)
        doc.add_paragraph(content)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)

    return buf

# ---------------- PAGE ----------------

st.title("📄 AI Resume Architect")

mode = st.radio(
    "Choose Mode",
    ["Fill Form", "Generate from Prompt"]
)

col1, col2 = st.columns(2)

# ---------------- FORM MODE ----------------

if mode == "Fill Form":

    with col1:

        st.subheader("Your Information")

        name = st.text_input("Full Name")
        job = st.text_input("Job Title")

        email = st.text_input("Email")
        phone = st.text_input("Phone")
        loc = st.text_input("Location")

        summary = st.text_area("About You")
        edu = st.text_area("Education")
        exp = st.text_area("Experience")
        skills = st.text_area("Skills")

        generate = st.button("Generate Resume")

    with col2:

        if generate:

            with st.spinner("Improving text..."):

                improved_summary = ask_ai(
                    f"Improve this resume summary professionally: {summary}"
                )

                improved_exp = ask_ai(
                    f"Improve this work experience: {exp}"
                )

                st.markdown(f"## {name}")
                st.write(job)
                st.write(f"{phone} | {email} | {loc}")

                st.subheader("Summary")
                st.write(clean(improved_summary))

                st.subheader("Education")
                st.write(edu)

                st.subheader("Experience")
                st.write(clean(improved_exp))

                st.subheader("Skills")
                st.write(skills)

                data = {
                    "name": name,
                    "job": job,
                    "email": email,
                    "phone": phone,
                    "loc": loc,
                    "sum": clean(improved_summary),
                    "edu": edu,
                    "exp": clean(improved_exp),
                    "skills": skills
                }

                file = create_docx(data)

                st.download_button(
                    "Download CV",
                    data=file,
                    file_name=f"{name}_resume.docx"
                )

# ---------------- PROMPT MODE ----------------

else:

    prompt = st.text_area(
        "Describe yourself and the job you want"
    )

    btn = st.button("Generate Resume with AI")

    if btn:

        with st.spinner("Creating resume..."):

            result = generate_from_prompt(prompt)

            st.write(result)
