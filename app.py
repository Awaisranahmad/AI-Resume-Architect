import streamlit as st
import requests
from PIL import Image
import base64
import io
import re

# --- 1. API Config ---
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="AI Resume Architect Pro", page_icon="📄", layout="wide")

# --- 2. CSS (Final Solid Version) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f7f9; }
    .cv-preview-container { 
        background: white; padding: 40px; border: 1px solid #ddd; border-radius: 4px;
        font-family: 'Arial', sans-serif; color: #000; margin: auto; line-height: 1.6;
    }
    .name-header { color: #1e3a8a; font-size: 30px; font-weight: bold; border-bottom: 3px solid #1e3a8a; margin-bottom: 5px; }
    .contact-info { font-size: 14px; margin-bottom: 20px; color: #555; font-weight: bold; }
    .sec-title { color: #1e3a8a; font-size: 18px; font-weight: bold; margin-top: 20px; text-transform: uppercase; border-bottom: 1px solid #eee; }
    .sec-content { font-size: 15px; margin-top: 5px; white-space: pre-line; color: #333; }
</style>
""", unsafe_allow_html=True)

# --- 3. Robust Functions ---
def clean_ai_text(text):
    # AI agar ```html ya tags wapas kare to unko hatane ke liye
    clean = re.sub(r'```[a-z]*', '', text)
    clean = clean.replace('```', '').strip()
    return clean

def ai_humanizer(text, label):
    if not text or len(text) < 5: return text
    try:
        prompt = f"Professional resume {label} bullet points (No intro, no tags): {text}"
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        res_json = response.json()
        if isinstance(res_json, list):
            raw_out = res_json[0].get('generated_text', text)
            result = raw_out.split(text)[-1] if text in raw_out else raw_out
            return clean_ai_text(result)
        return text
    except:
        return text

def get_img_64(file):
    if file:
        img = Image.open(file)
        img.thumbnail((120, 120))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

# --- 4. Sidebar Form ---
st.title("🛡️ AI Resume Architect")

col_in, col_out = st.columns([1, 1.3])

with col_in:
    with st.form("cv_form"):
        u_name = st.text_input("Full Name", "RANA AWAIS AHMAD")
        u_email = st.text_input("Email", "awais@example.com")
        u_phone = st.text_input("Phone", "+92 300 1234567")
        u_pic = st.file_uploader("Photo", type=['png', 'jpg'])
        u_edu = st.text_area("Education", "BS Computer Science, 2024")
        u_exp = st.text_area("Experience", "Describe your projects or work here...")
        u_skills = st.text_input("Skills", "Python, React, SQL")
        submit = st.form_submit_button("🚀 GENERATE RESUME")

# --- 5. Output Render & Download ---
if submit:
    with st.spinner("Humanizing Content..."):
        img_b64 = get_img_64(u_pic)
        final_exp = ai_humanizer(u_exp, "experience")
        final_edu = ai_humanizer(u_edu, "education")
        
        # HTML Content
        cv_html = f"""
        <div class="cv-preview-container">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div class="name-header">{u_name.upper()}</div>
                    <div class="contact-info">📧 {u_email} | 📞 {u_phone}</div>
                </div>
                {f'<img src="data:image/png;base64,{img_b64}" style="width:100px; height:100px; border-radius:8px; border:2px solid #1e3a8a;">' if img_b64 else ""}
            </div>
            
            <div class="sec-title">Education</div>
            <div class="sec-content">{final_edu}</div>
            
            <div class="sec-title">Professional Experience</div>
            <div class="sec-content">{final_exp}</div>
            
            <div class="sec-title">Technical Skills</div>
            <div class="sec-content">{u_skills}</div>
        </div>
        """
        
        with col_out:
            st.markdown(cv_html, unsafe_allow_html=True)
            
            # --- DOWNLOAD OPTION ---
            full_html = f"<html><head><style>body{{font-family:Arial; padding:50px;}} .name-header{{color:#1e3a8a; font-size:30px; border-bottom:3px solid #1e3a8a;}} .sec-title{{color:#1e3a8a; font-size:18px; font-weight:bold; margin-top:20px; border-bottom:1px solid #eee;}}</style></head><body>{cv_html}</body></html>"
            st.download_button(
                label="📥 DOWNLOAD CV AS HTML",
                data=full_html,
                file_name=f"{u_name}_Resume.html",
                mime="text/html",
                use_container_width=True
            )
            st.success("Tip: Open the downloaded file and press Ctrl+P to Save as PDF!")
else:
    with col_out:
        st.info("Preview will show here after clicking Generate.")
