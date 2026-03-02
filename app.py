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

# --- 2. CSS (Clean & Minimalist) ---
st.markdown("""
<style>
    .stApp { background-color: white; }
    .cv-preview { 
        padding: 40px; color: black; font-family: 'Arial', sans-serif;
        max-width: 800px; margin: auto; border: 1px solid #eee;
    }
    .name-h { font-size: 32px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .title-h { font-size: 18px; text-align: center; color: #555; margin-bottom: 10px; }
    .contact-h { font-size: 13px; text-align: center; border-bottom: 1px solid black; padding-bottom: 15px; margin-bottom: 20px; }
    .sec-h { font-size: 16px; font-weight: bold; text-transform: uppercase; margin-top: 20px; border-bottom: 1px solid #ccc; }
    .content-p { font-size: 14px; margin-top: 8px; white-space: pre-wrap; text-align: justify; }
</style>
""", unsafe_allow_html=True)

# --- 3. Better Cleaning Logic ---
def clean_ai_output(raw_result, original_input):
    # AI agar prompt repeat kare to usay remove karo
    clean = raw_result.replace(original_input, "")
    # Har kism ke HTML tags ko remove karo
    clean = re.sub('<[^<]+?>', '', clean)
    # Markdown code blocks (```) ko remove karo
    clean = clean.replace("```html", "").replace("```", "").strip()
    return clean

def ai_call(text, category):
    if not text or len(text) < 5: return text
    try:
        prompt = f"Rewrite this resume {category} professionally. No intro, no tags: {text}"
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        res = response.json()
        if isinstance(res, list):
            full_out = res[0].get('generated_text', text)
            return clean_ai_output(full_out, prompt)
        return text
    except:
        return text

# --- 4. Word Export ---
def make_docx(d):
    doc = Document()
    n = doc.add_paragraph()
    n.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = n.add_run(d['name'].upper())
    run.font.size = Pt(22)
    run.bold = True
    
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.add_run(d['job'])
    
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.add_run(f"{d['phone']} | {d['email']} | {d['loc']}")
    
    for sec in [('About Me', d['sum']), ('Education', d['edu']), ('Experience', d['exp']), ('Skills', d['skills'])]:
        doc.add_heading(sec[0].upper(), level=1)
        doc.add_paragraph(sec[1])
        
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 5. Main UI ---
st.title("📄 Resume Architect (Sebastian Style)")

c1, c2 = st.columns([1, 1.2])

with c1:
    with st.expander("👤 Personal Details", expanded=True):
        u_name = st.text_input("Name", "Sebastian Bennett")
        u_job = st.text_input("Title", "Professional Accountant")
        u_email = st.text_input("Email", "hello@site.com")
        u_phone = st.text_input("Phone", "+123-456-7890")
        u_loc = st.text_input("Location", "Any City, USA")
    
    with st.expander("📝 Content", expanded=True):
        u_sum = st.text_area("About Me", "I am a motivated accountant...")
        u_edu = st.text_area("Education", "University Name | 2026")
        u_exp = st.text_area("Experience", "Senior Accountant at Salford & Co.")
        u_skills = st.text_area("Skills", "Auditing, Tax, SQL")

    gen = st.button("🚀 BUILD PROFESSIONAL CV")

with c2:
    if gen:
        with st.spinner("Humanizing..."):
            # Process content separately to avoid mixing tags
            h_sum = ai_call(u_sum, "summary")
            h_exp = ai_call(u_exp, "experience")
            
            # Web Preview
            st.markdown(f"""
            <div class="cv-preview">
                <div class="name-h">{u_name.upper()}</div>
                <div class="title-h">{u_job}</div>
                <div class="contact-h">📞 {u_phone} | 📧 {u_email} | 📍 {u_loc}</div>
                
                <div class="sec-h">About Me</div>
                <div class="content-p">{h_sum}</div>
                
                <div class="sec-h">Education</div>
                <div class="content-p">{u_edu}</div>
                
                <div class="sec-h">Work Experience</div>
                <div class="content-p">{h_exp}</div>
                
                <div class="sec-h">Skills</div>
                <div class="content-p">{u_skills}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Download Word
            data = {'name':u_name, 'job':u_job, 'email':u_email, 'phone':u_phone, 'loc':u_loc, 'sum':h_sum, 'edu':u_edu, 'exp':h_exp, 'skills':u_skills}
            word_file = make_docx(data)
            st.download_button("📥 DOWNLOAD AS WORD (.DOCX)", data=word_file, file_name=f"{u_name}_CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    else:
        st.info("Preview yahan nazar aaye ga.")
