import streamlit as st
import requests
from PIL import Image
import base64
import io

# --- 1. API Config ---
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
# Ensure HF_TOKEN is in your Streamlit Secrets
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="AI Resume Architect Pro", page_icon="📄", layout="wide")

# --- 2. CSS (Simplified to avoid rendering bugs) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f7f9; }
    .cv-preview-container { 
        background: white; 
        padding: 40px; 
        border: 1px solid #ddd;
        border-radius: 4px;
        font-family: 'Times New Roman', serif;
        color: #000;
        margin: auto;
    }
    .name-header { color: #1e3a8a; font-size: 28px; font-weight: bold; border-bottom: 2px solid #1e3a8a; }
    .contact-info { font-size: 13px; margin-bottom: 20px; color: #444; }
    .sec-title { color: #1e3a8a; font-size: 18px; font-weight: bold; margin-top: 15px; text-transform: uppercase; border-bottom: 1px solid #ccc; }
    .sec-content { font-size: 14px; margin-top: 5px; white-space: pre-line; }
</style>
""", unsafe_allow_html=True)

# --- 3. Functions ---
def get_img_64(file):
    if file:
        img = Image.open(file)
        img.thumbnail((120, 120))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

def ai_humanizer(text, label):
    if not text or len(text) < 5: return text
    try:
        prompt = f"Professional resume {label}: {text}"
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        res_json = response.json()
        if isinstance(res_json, list):
            raw_out = res_json[0].get('generated_text', text)
            return raw_out.split(text)[-1].strip() if text in raw_out else raw_out
        return text
    except:
        return text

# --- 4. Sidebar Form ---
st.title("🛡️ AI Resume Architect")

col_left, col_right = st.columns([1, 1.2])

with col_left:
    with st.expander("👤 Personal Details", expanded=True):
        u_name = st.text_input("Name", "ANA AWAIS AHMAD")
        u_email = st.text_input("Email", "awais@example.com")
        u_phone = st.text_input("Phone", "+92 300 1234567")
        u_pic = st.file_uploader("Photo", type=['png', 'jpg'])
    
    with st.expander("📝 Content", expanded=True):
        u_edu = st.text_area("Education", "BS Computer Science, 2024")
        u_exp = st.text_area("Experience", "Describe your work here...")
        u_skills = st.text_input("Skills", "Python, SQL, React")

    btn = st.button("🚀 GENERATE RESUME", use_container_width=True)

# --- 5. Output Preview (The Fix) ---
with col_right:
    if btn:
        with st.spinner("Rendering..."):
            img_b64 = get_img_64(u_pic)
            
            # Simple AI Call
            final_exp = ai_humanizer(u_exp, "experience")
            
            # Using a single clean HTML Block
            cv_html = f"""
            <div class="cv-preview-container">
                <div class="name-header">{u_name.upper()}</div>
                <div class="contact-info">📧 {u_email} | 📞 {u_phone}</div>
                
                {"<img src='data:image/png;base64," + img_b64 + "' style='float:right; width:80px; margin-top:-60px; border-radius:5px;'>" if img_b64 else ""}
                
                <div class="sec-title">Education</div>
                <div class="sec-content">{u_edu}</div>
                
                <div class="sec-title">Professional Experience</div>
                <div class="sec-content">{final_exp}</div>
                
                <div class="sec-title">Technical Skills</div>
                <div class="sec-content">{u_skills}</div>
            </div>
            """
            st.markdown(cv_html, unsafe_allow_html=True)
            st.success("Print (Ctrl+P) to save as PDF")
    else:
        st.info("Preview will show here.")
