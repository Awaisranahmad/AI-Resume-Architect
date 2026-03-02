import streamlit as st
import requests
from PIL import Image
import base64
import io
import time

# --- 1. Hugging Face API Config ---
# Mistral-7B is free and powerful for professional rewriting
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="AI Resume Architect", page_icon="📄", layout="wide")

# --- 2. Professional CSS Styling ---
st.markdown("""
<style>
    .stApp { background-color: #f0f4f8; color: #1e3a8a; }
    .main-title { font-size: 36px; font-weight: 800; text-align: center; color: #1e3a8a; margin-bottom: 10px; }
    .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 5px solid #3b82f6; }
    .cv-preview { 
        background: white; 
        padding: 40px; 
        border-radius: 5px; 
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        color: #333;
        font-family: 'Helvetica', sans-serif;
        line-height: 1.6;
    }
    .section-header { color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 5px; margin-top: 20px; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# --- 3. Helper Functions ---
def humanize_with_hf(text):
    if not text or len(text) < 10: return text
    
    payload = {
        "inputs": f"Rewrite the following resume experience to be professional, impactful, and sound 100% written by a human expert. Avoid AI cliches like 'spearheaded' or 'synergy'. Use natural active verbs: {text}",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        output = response.json()
        
        # Check if model is still loading
        if "error" in output and "loading" in output["error"]:
            st.warning("Hugging Face model is waking up... retrying in 10s")
            time.sleep(10)
            return humanize_with_hf(text)
            
        if isinstance(output, list):
            gen_text = output[0].get('generated_text', text)
            # Remove the prompt from the result
            return gen_text.split("human expert.")[-1].strip()
        return text
    except:
        return text

def get_image_base64(uploaded_file):
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        # Force resize to keep it professional
        img.thumbnail((150, 150))
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

# --- 4. Main UI Layout ---
st.markdown("<div class='main-title'>🛡️ AI Resume Architect Pro</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Professional • Humanized • ATS-Friendly</p>", unsafe_allow_html=True)

col_form, col_view = st.columns([1, 1.2], gap="large")

with col_form:
    st.markdown("### 🛠️ Resume Details")
    
    # Personal Info Card
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("👤 **Personal Information**")
        name = st.text_input("Full Name", placeholder="e.g., Muhammad Ali")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        
        user_img = st.file_uploader("Profile Picture (Max 1MB)", type=['jpg', 'jpeg', 'png'])
        if user_img and user_img.size > 1024 * 1024:
            st.error("Image size too large! Please use a file under 1MB.")
            user_img = None
        st.markdown("</div>", unsafe_allow_html=True)

    # Experience & Education Card
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("🎓 **Academic & Professional**")
        edu = st.text_area("Education (Degree, University, Year)", height=100)
        exp = st.text_area("Work Experience (Raw or Bullet Points)", height=150, placeholder="Explain what you did in simple words...")
        st.markdown("</div>", unsafe_allow_html=True)

    # Skills & Projects Card
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("🚀 **Skills & Projects (Optional)**")
        skills = st.text_input("Skills (Comma separated)", placeholder="Python, Data Analysis, Leadership")
        projects = st.text_area("Key Projects", height=100)
        st.markdown("</div>", unsafe_allow_html=True)

    generate_btn = st.button("🚀 GENERATE HUMANIZED RESUME", use_container_width=True)

# --- 5. CV Generation & Preview ---
with col_view:
    st.markdown("### 📄 Professional Preview")
    
    if generate_btn and name:
        with st.spinner("AI is humanizing your content..."):
            # Process Image
            img_b64 = get_image_base64(user_img)
            
            # Humanize Text using Hugging Face
            human_exp = humanize_with_hf(exp)
            human_proj = humanize_with_hf(projects)

            # CV HTML Template
            cv_html = f"""
            <div class="cv-preview">
                <table style="width:100%; border-collapse: collapse;">
                    <tr>
                        <td style="vertical-align: top;">
                            <h1 style="margin:0; color:#1e3a8a; font-size:28px;">{name.upper()}</h1>
                            <p style="margin:5px 0; color:#555;">📧 {email} | 📞 {phone}</p>
                        </td>
                        <td style="text-align: right; vertical-align: top;">
                            {f'<img src="data:image/png;base64,{img_b64}" style="width:110px; height:110px; border-radius:50%; border:3px solid #3b82f6; object-fit: cover;">' if img_b64 else ""}
                        </td>
                    </tr>
                </table>

                <h3 class="section-header">Education</h3>
                <p style="white-space: pre-wrap;">{edu}</p>

                {f'<h3 class="section-header">Professional Experience</h3><p style="white-space: pre-wrap;">{human_exp}</p>' if exp else ""}
                
                {f'<h3 class="section-header">Technical Skills</h3><p>{skills}</p>' if skills else ""}
                
                {f'<h3 class="section-header">Key Projects</h3><p style="white-space: pre-wrap;">{human_proj}</p>' if projects else ""}
            </div>
            """
            st.markdown(cv_html, unsafe_allow_html=True)
            st.success("✅ Resume Ready! Right-click -> Print -> Save as PDF.")
            
    elif generate_btn and not name:
        st.error("Please enter your name at least!")
    else:
        st.info("Your professional resume will appear here once you click Generate.")

st.write("---")
st.caption("AI Resume Architect v1.0 | Powered by Hugging Face Mistral-7B | Secure & Humanized")
