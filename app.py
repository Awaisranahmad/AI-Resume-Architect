import streamlit as st
import requests
from PIL import Image
import io
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- 1. API Config ---
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Professional Resume Architect", layout="wide")

# --- 2. Professional CSS for Preview ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .cv-body { 
        padding: 40px; color: #000; font-family: 'Helvetica', sans-serif;
        max-width: 800px; margin: auto; border: 1px solid #eee;
    }
    .cv-name { font-size: 32px; font-weight: bold; text-align: center; text-transform: uppercase; margin-bottom: 5px; }
    .cv-title { font-size: 18px; text-align: center; color: #444; margin-bottom: 15px; }
    .cv-contact { font-size: 12px; text-align: center; border-bottom: 1px solid #000; padding-bottom: 15px; margin-bottom: 20px; }
    .sec-h { font-size: 16px; font-weight: bold; text-transform: uppercase; margin-top: 20px; border-bottom: 1px solid #ccc; padding-bottom: 2px; }
    .sec-content { font-size: 13px; margin-top: 8px; line-height: 1.4; white-space: pre-line; text-align: justify; }
</style>
""", unsafe_allow_html=True)

# --- 3. Robust Humanizer & Word Export ---
def ai_humanizer(text, label):
    if not text or len(text) < 5: return text
    try:
        # Prompt ko strict rakha hai taake koi tags na aayein
        prompt = f"Rewrite this resume {label} to be professional and humanized. Use clear sentences. No intro, no HTML tags. Content: {text}"
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 250}})
        res = response.json()
        out = res[0]['generated_text'] if isinstance(res, list) else text
        # Cleanup: AI ka repeat kiya hua prompt hatana
        final = out.split(text)[-1].strip() if text in out else out
        return re.sub('<[^<]+?>', '', final) # Extra safety for HTML tags
    except:
        return text

def create_professional_docx(data):
    doc = Document()
    
    # Name & Job Title
    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = name_p.add_run(data['name'].upper())
    run.font.size = Pt(24)
    run.bold = True
    
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = title_p.add_run(data['job_title'])
    run_t.font.size = Pt(14)
    
    # Contact Info
    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.add_run(f"📞 {data['phone']}  |  📧 {data['email']}  |  📍 {data['location']}")
    
    # Sections Helper
    def add_section(title, content):
        h = doc.add_heading(title.upper(), level=1)
        doc.add_paragraph(content)

    add_section("About Me", data['summary'])
    add_section("Education", data['edu'])
    add_section("Work Experience", data['exp'])
    add_section("Skills", data['skills'])

    target = io.BytesIO()
    doc.save(target)
    target.seek(0)
    return target

# --- 4. Sidebar Input ---
st.title("📄 Professional Resume Builder")

col1, col2 = st.columns([1, 1.2])

with col1:
    with st.expander("👤 Header Information", expanded=True):
        u_name = st.text_input("Full Name", "Sebastian Bennett")
        u_job = st.text_input("Professional Title", "Professional Accountant")
        u_email = st.text_input("Email", "hello@reallygreatsite.com")
        u_phone = st.text_input("Phone", "+123-456-7890")
        u_loc = st.text_input("Location", "123 Anywhere St., Any City")
    
    with st.expander("📝 Resume Content", expanded=True):
        u_sum = st.text_area("About Me (Summary)", "Highly motivated professional with experience in...")
        u_edu = st.text_area("Education", "Borcelle University | 2026-2030")
        u_exp = st.text_area("Work Experience", "Senior Accountant at Salford & Co.")
        u_skills = st.text_area("Skills", "Auditing, Financial Reporting, SQL")

    generate = st.button("🚀 GENERATE HUMANIZED RESUME")

# --- 5. Professional Preview & Download ---
with col2:
    if generate:
        with st.spinner("Humanizing your career story..."):
            # AI Processing
            h_sum = ai_humanizer(u_sum, "summary")
            h_exp = ai_humanizer(u_exp, "experience")
            
            # Web Preview
            st.markdown(f"""
            <div class="cv-body">
                <div class="cv-name">{u_name}</div>
                <div class="cv-title">{u_job}</div>
                <div class="cv-contact">📞 {u_phone}  |  📧 {u_email}  |  📍 {u_loc}</div>
                
                <div class="sec-h">About Me</div>
                <div class="sec-content">{h_sum}</div>
                
                <div class="sec-h">Education</div>
                <div class="sec-content">{u_edu}</div>
                
                <div class="sec-h">Work Experience</div>
                <div class="sec-content">{h_exp}</div>
                
                <div class="sec-h">Skills</div>
                <div class="sec-content">{u_skills}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Word File
            cv_data = {
                'name': u_name, 'job_title': u_job, 'email': u_email, 
                'phone': u_phone, 'location': u_loc, 'summary': h_sum,
                'edu': u_edu, 'exp': h_exp, 'skills': u_skills
            }
            docx_file = create_professional_docx(cv_data)
            
            st.download_button(
                label="📥 DOWNLOAD PROFESSIONAL WORD FILE",
                data=docx_file,
                file_name=f"{u_name}_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
    else:
        st.info("Fill the details and click Generate to see the professional layout.")
