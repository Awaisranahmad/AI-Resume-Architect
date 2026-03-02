import streamlit as st
import requests
from PIL import Image
import base64
import io
import re
from docx import Document
from docx.shared import Inches, Pt

# --- 1. API Config ---
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="AI Resume Architect Pro", page_icon="📄", layout="wide")

# --- 2. CSS for UI Only ---
st.markdown("""
<style>
    .stApp { background-color: #f4f7f9; }
    .cv-preview { 
        background: white; padding: 30px; border-radius: 5px; border: 1px solid #ddd;
        color: #000; font-family: 'Arial'; line-height: 1.5;
    }
    .name-h { color: #1e3a8a; font-size: 26px; font-weight: bold; border-bottom: 2px solid #1e3a8a; }
    .sec-h { color: #1e3a8a; font-size: 16px; font-weight: bold; margin-top: 15px; text-transform: uppercase; border-bottom: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# --- 3. Functions ---
def clean_ai_response(raw_text):
    # Sab se pehle tags aur markdown code blocks khatam karo
    clean = re.sub(r'<.*?>', '', raw_text)
    clean = re.sub(r'```.*?```', '', clean, flags=re.DOTALL)
    # Agar AI ne prompt repeat kiya ho to usay kaato
    if "Professional resume" in clean:
        clean = clean.split(":")[-1]
    return clean.strip()

def ai_humanizer(text, label):
    if not text or len(text) < 5: return text
    try:
        payload = {"inputs": f"Professional resume {label} bullet points: {text}", "parameters": {"max_new_tokens": 200}}
        response = requests.post(API_URL, headers=headers, json=payload)
        res_json = response.json()
        if isinstance(res_json, list):
            raw = res_json[0].get('generated_text', text)
            # Remove original input if AI repeated it
            processed = raw.replace(f"Professional resume {label} bullet points: {text}", "")
            return clean_ai_response(processed)
        return text
    except:
        return text

def create_docx(name, email, phone, edu, exp, skills):
    doc = Document()
    # Name
    hdr = doc.add_heading(name.upper(), 0)
    # Contact
    p = doc.add_paragraph()
    p.add_run(f"Email: {email} | Phone: {phone}").italic = True
    
    # Sections
    doc.add_heading('Education', level=1)
    doc.add_paragraph(edu)
    
    doc.add_heading('Experience', level=1)
    doc.add_paragraph(exp)
    
    doc.add_heading('Skills', level=1)
    doc.add_paragraph(skills)
    
    target_stream = io.BytesIO()
    doc.save(target_stream)
    target_stream.seek(0)
    return target_stream

# --- 4. Sidebar Form ---
st.title("🛡️ AI Resume Architect")

col_in, col_out = st.columns([1, 1.2])

with col_in:
    with st.form("main_form"):
        u_name = st.text_input("Full Name", "RANA AWAIS AHMAD")
        u_email = st.text_input("Email", "awais@example.com")
        u_phone = st.text_input("Phone", "+92 300 1234567")
        u_edu = st.text_area("Education", "BS Computer Science, 2024")
        u_exp = st.text_area("Experience", "Describe your work...")
        u_skills = st.text_input("Skills", "Python, React, SQL")
        submit = st.form_submit_button("🚀 GENERATE & HUMANIZE")

# --- 5. Output Render ---
if submit:
    with st.spinner("AI is rewriting..."):
        # Humanizing process
        final_exp = ai_humanizer(u_exp, "experience")
        final_edu = ai_humanizer(u_edu, "education")
        
        with col_out:
            # Preview on Web
            st.markdown(f"""
            <div class="cv-preview">
                <div class="name-h">{u_name.upper()}</div>
                <p>📧 {u_email} | 📞 {u_phone}</p>
                <div class="sec-h">Education</div>
                <p>{final_edu}</p>
                <div class="sec-h">Professional Experience</div>
                <p>{final_exp}</p>
                <div class="sec-h">Technical Skills</div>
                <p>{u_skills}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- WORD DOWNLOAD ---
            docx_file = create_docx(u_name, u_email, u_phone, final_edu, final_exp, u_skills)
            st.download_button(
                label="📥 DOWNLOAD AS WORD (.DOCX)",
                data=docx_file,
                file_name=f"{u_name}_CV.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
else:
    with col_out:
        st.info("Your professional CV preview will appear here.")
