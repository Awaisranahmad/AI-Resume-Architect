import streamlit as st
import requests
from PIL import Image
import base64
import io
import time

# --- 1. Hugging Face API Config ---
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="AI Resume Architect Pro", page_icon="📄", layout="wide")

# --- 2. Enhanced CSS (Fixing the layout issues) ---
st.markdown("""
<style>
    .stApp { background-color: #f4f7f9; }
    .cv-preview { 
        background: white; 
        padding: 50px; 
        border-radius: 2px; 
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
        color: #333;
        font-family: 'Garamond', serif;
        max-width: 850px;
        margin: auto;
    }
    .cv-header { border-bottom: 3px solid #1e3a8a; padding-bottom: 10px; margin-bottom: 20px; }
    .cv-name { font-size: 32px; color: #1e3a8a; font-weight: bold; margin: 0; }
    .cv-contact { font-size: 14px; color: #555; margin: 5px 0; }
    .section-title { 
        font-size: 18px; 
        color: #1e3a8a; 
        font-weight: bold; 
        text-transform: uppercase; 
        margin-top: 25px; 
        border-bottom: 1px solid #ddd;
    }
    .cv-content { font-size: 15px; line-height: 1.5; margin-top: 8px; white-space: pre-wrap; }
    .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 3. Better Humanizer (Mistral Prompt Fix) ---
def humanize_with_hf(text, section_name):
    if not text or len(text) < 3: return text
    
    # Prompt ko zyada clear kiya hai taake AI dummy text ko bhi handle kare
    prompt = f"Rewrite this {section_name} for a resume. Make it professional, bulleted, and human-like. Text: {text}"
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 300}})
        output = response.json()
        
        if isinstance(output, list):
            res = output[0].get('generated_text', text)
            # Sirf AI ka likha hua part nikalna
            return res.split(text)[-1].strip() if text in res else res
        return text
    except:
        return text

def get_base64(file):
    if file:
        img = Image.open(file)
        img.thumbnail((150, 150))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

# --- 4. Sidebar/Form UI ---
st.markdown("<h1 style='text-align:center; color:#1e3a8a;'>🛡️ AI Resume Architect</h1>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("🛠️ Build Your Profile")
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        name = st.text_input("Full Name", "ANA AWAIS AHMAD")
        email = st.text_input("Email", "awais@example.com")
        phone = st.text_input("Phone", "+92 300 1234567")
        pic = st.file_uploader("Photo (Max 1MB)", type=['jpg','png'])
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        edu = st.text_area("Education", "BS Computer Science, University Name, 2024")
        exp = st.text_area("Work Experience", "Worked on web projects and database management.")
        skills = st.text_input("Skills", "Python, SQL, Communication")
        st.markdown("</div>", unsafe_allow_html=True)

    gen = st.button("🚀 GENERATE PROFESSIONAL CV", use_container_width=True)

# --- 5. CV Generation Logic ---
with col_out:
    if gen:
        with st.spinner("Processing Professional Layout..."):
            img_code = get_base64(pic)
            # Section-wise humanizing
            h_exp = humanize_with_hf(exp, "Work Experience")
            h_edu = humanize_with_hf(edu, "Education")

            cv_html = f"""
            <div class="cv-preview">
                <div class="cv-header">
                    <table style="width:100%;">
                        <tr>
                            <td>
                                <div class="cv-name">{name.upper()}</div>
                                <div class="cv-contact">📧 {email} | 📞 {phone}</div>
                            </td>
                            <td style="text-align:right;">
                                {f'<img src="data:image/png;base64,{img_code}" style="width:100px; height:100px; border-radius:5px; border:1px solid #ddd;">' if img_code else ""}
                            </td>
                        </tr>
                    </table>
                </div>

                <div class="section-title">Education</div>
                <div class="cv-content">{h_edu}</div>

                {f'<div class="section-title">Professional Experience</div><div class="cv-content">{h_exp}</div>' if exp else ""}
                
                {f'<div class="section-title">Technical Skills</div><div class="cv-content">{skills}</div>' if skills else ""}
            </div>
            """
            st.markdown(cv_html, unsafe_allow_html=True)
            st.success("✅ Ready! Use 'Print' (Ctrl+P) to save as PDF.")
    else:
        st.info("Preview will appear here.")
