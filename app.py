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

# --- 2. CSS (Clean & Solid) ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    .resume-paper {
        background: white; padding: 50px; border: 1px solid #ddd;
        font-family: 'Arial', sans-serif; max-width: 800px; margin: auto;
    }
    .header-name { font-size: 34px; font-weight: bold; text-align: center; margin-bottom: 0; }
    .header-title { font-size: 18px; text-align: center; color: #555; margin-bottom: 10px; }
    .header-contact { font-size: 13px; text-align: center; border-bottom: 2px solid black; padding-bottom: 15px; margin-bottom: 25px; }
    .section-h { font-size: 18px; font-weight: bold; text-transform: uppercase; margin-top: 25px; border-bottom: 1px solid #eee; }
    .text-body { font-size: 14px; margin-top: 10px; line-height: 1.6; white-space: pre-wrap; }
</style>
""", unsafe_allow_html=True)

# --- 3. Functions ---
def clean_text(text):
    # AI ke kisi bhi kism ke HTML tags ko dho dalo
    clean = re.sub(r'<.*?>', '', text)
    clean = clean.replace("```html", "").replace("```", "").strip()
    return clean

def get_ai_response(text, category):
    if not text or len(text) < 3: return text
    try:
        # Strict instructions for AI: NO HTML!
        prompt = f"Rewrite this resume {category} in professional plain text. No tags, no intro: {text}"
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        res = response.json()
        out = res[0]['generated_text'] if isinstance(res, list) else text
        # Remove prompt from output
        final = out.split(text)[-1].strip() if text in out else out
        return clean_text(final)
    except:
        return clean_text(text)

def build_docx(d):
    doc = Document()
    # Name & Title
    n = doc.add_paragraph()
    n.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = n.add_run(d['name'].upper())
    run.font.size = Pt(24); run.bold = True
    
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.add_run(d['job']).font.size = Pt(14)
    
    # Contact
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.add_run(f"{d['phone']} | {d['email']} | {d['loc']}").font.size = Pt(10)
    
    # Sections
    sections = [("About Me", d['sum']), ("Education", d['edu']), ("Experience", d['exp']), ("Skills", d['skills'])]
    for title, content in sections:
        doc.add_heading(title.upper(), level=1)
        doc.add_paragraph(content)
        
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 4. Sidebar Input ---
st.title("📄 AI Resume Architect (Pro)")

c1, c2 = st.columns([1, 1.2])

with c1:
    with st.expander("👤 Header Details", expanded=True):
        u_name = st.text_input("Full Name", "Sebastian Bennett")
        u_job = st.text_input("Title", "Professional Accountant")
        u_email = st.text_input("Email", "hello@reallygreatsite.com")
        u_phone = st.text_input("Phone", "+123-456-7890")
        u_loc = st.text_input("Location", "Any City, USA")
    
    with st.expander("📝 Content", expanded=True):
        u_sum = st.text_area("About Me", "I am a motivated accountant with 5 years experience...")
        u_edu = st.text_area("Education", "Borcelle University | 2026-2030")
        u_exp = st.text_area("Experience", "Senior Accountant at Salford & Co.")
        u_skills = st.text_area("Skills", "Auditing, Financial Reporting, Tax Strategy")

    btn = st.button("🚀 GENERATE HUMANIZED CV")

# --- 5. Preview & Download ---
with c2:
    if btn:
        with st.spinner("Refining content..."):
            h_sum = get_ai_response(u_sum, "summary")
            h_exp = get_ai_response(u_exp, "work experience")
            
            # Web Preview (The Sebastian Style)
            st.markdown(f"""
            <div class="resume-paper">
                <div class="header-name">{u_name.upper()}</div>
                <div class="header-title">{u_job}</div>
                <div class="header-contact">{u_phone}  |  {u_email}  |  {u_loc}</div>
                
                <div class="section-h">About Me</div>
                <div class="text-body">{h_sum}</div>
                
                <div class="section-h">Education</div>
                <div class="text-body">{u_edu}</div>
                
                <div class="section-h">Work Experience</div>
                <div class="text-body">{h_exp}</div>
                
                <div class="section-h">Skills</div>
                <div class="text-body">{u_skills}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Word Download Logic
            cv_dict = {'name':u_name, 'job':u_job, 'email':u_email, 'phone':u_phone, 'loc':u_loc, 'sum':h_sum, 'edu':u_edu, 'exp':h_exp, 'skills':u_skills}
            word_file = build_docx(cv_dict)
            st.download_button("📥 DOWNLOAD AS WORD (.DOCX)", data=word_file, file_name=f"{u_name}_CV.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    else:
        st.info("Fill the details and click Generate.")
