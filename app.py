import streamlit as st
import requests
from PIL import Image
import io
import re
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- 1. API Config ---
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Professional Resume Architect", layout="wide")

# --- 2. Robust Cleaning & AI Logic ---
def clean_and_humanize(text, label):
    if not text or len(text) < 3: return text
    try:
        prompt = f"Rewrite this resume {label} to be professional and human-like. Use plain text only, no tags: {text}"
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        res = response.json()
        out = res[0]['generated_text'] if isinstance(res, list) else text
        # Remove original prompt and any weird tags
        final = out.split(text)[-1].strip() if text in out else out
        return re.sub(r'<.*?>', '', final) 
    except:
        return text

def create_docx(d):
    doc = Document()
    n = doc.add_paragraph()
    n.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = n.add_run(d['name'].upper())
    run.font.size = Pt(24); run.bold = True
    
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.add_run(d['job']).font.size = Pt(14)
    
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.add_run(f"{d['phone']} | {d['email']} | {d['loc']}").font.size = Pt(10)
    
    for title, content in [("About Me", d['sum']), ("Education", d['edu']), ("Work Experience", d['exp']), ("Skills", d['skills'])]:
        doc.add_heading(title.upper(), level=1)
        doc.add_paragraph(content)
        
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 3. UI Layout ---
st.title("📄 AI Resume Architect (Sebastian Style)")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("👤 Your Details")
    u_name = st.text_input("Full Name", "Sebastian Bennett")
    u_job = st.text_input("Title", "Professional Accountant")
    u_email = st.text_input("Email", "hello@reallygreatsite.com")
    u_phone = st.text_input("Phone", "+123-456-7890")
    u_loc = st.text_input("Location", "Any City, USA")
    
    u_sum = st.text_area("About Me", "Experienced accountant specializing in tax...")
    u_edu = st.text_area("Education", "Borcelle University | 2026-2030")
    u_exp = st.text_area("Experience", "Senior Accountant at Salford & Co.")
    u_skills = st.text_area("Skills", "Auditing, Financial Reporting, Tax Strategy")

    btn = st.button("🚀 GENERATE PROFESSIONAL CV")

with col2:
    if btn:
        with st.spinner("Humanizing..."):
            h_sum = clean_and_humanize(u_sum, "summary")
            h_exp = clean_and_humanize(u_exp, "experience")
            
            # --- THE FIX: Using Markdown instead of HTML Strings ---
            st.markdown(f"<h1 style='text-align: center; color: #1e3a8a;'>{u_name.upper()}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 18px;'>{u_job}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;'>{u_phone} | {u_email} | {u_loc}</p>", unsafe_allow_html=True)
            
            st.subheader("ABOUT ME")
            st.write(h_sum)
            
            st.subheader("EDUCATION")
            st.write(u_edu)
            
            st.subheader("WORK EXPERIENCE")
            st.write(h_exp)
            
            st.subheader("SKILLS")
            st.write(u_skills)
            
            # Word Download
            cv_data = {'name':u_name, 'job':u_job, 'email':u_email, 'phone':u_phone, 'loc':u_loc, 'sum':h_sum, 'edu':u_edu, 'exp':h_exp, 'skills':u_skills}
            word_file = create_docx(cv_data)
            st.download_button("📥 DOWNLOAD AS WORD (.DOCX)", data=word_file, file_name=f"{u_name}_CV.docx", use_container_width=True)
    else:
        st.info("Input details and click Generate to see the clean layout.")
