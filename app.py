import streamlit as st
from groq import Groq  # New import

# --- API Config ---
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = st.secrets.get("HF_TOKEN", "")  # Safe access

# Groq setup
GROQ_CLIENT = None
if "GROQ_API_KEY" in st.secrets and st.secrets["GROQ_API_KEY"]:
    try:
        GROQ_CLIENT = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        st.error(f"Groq initialization failed: {e}")
else:
    st.warning("Groq API key not found in secrets. Falling back to Hugging Face (slower).")

# --- AI Query Function (Groq preferred) ---
def query_ai(prompt, model="llama-3.1-70b-versatile", temperature=0.75, max_tokens=1200):
    """
    Groq se pehle try → fast + better human-like output
    Fail hone pe Hugging Face fallback
    """
    if GROQ_CLIENT:
        try:
            chat_completion = GROQ_CLIENT.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,                  # Best models: llama-3.1-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it
                temperature=temperature,      # 0.7-0.9 = good randomness/human feel
                max_tokens=max_tokens,
                top_p=0.9,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            st.warning(f"Groq failed: {e}. Falling back to HF.")
    
    # Hugging Face fallback (old logic)
    if not HF_TOKEN:
        return "Error: No API tokens available."
    
    try:
        payload = {"inputs": prompt, "parameters": {"temperature": temperature, "max_new_tokens": max_tokens}}
        response = requests.post(HF_API_URL, headers={"Authorization": f"Bearer {HF_TOKEN}"}, json=payload)
        res = response.json()
        if isinstance(res, list) and res:
            out = res[0].get('generated_text', '')
            # Clean prompt echo
            if prompt in out:
                out = out.split(prompt)[-1].strip()
            return re.sub(r'<.*?>|\[.*?\]', '', out)
        return ""
    except Exception as e:
        st.error(f"HF fallback also failed: {e}")
        return ""

# Humanize function (same, but ab Groq use karega)
def humanize_text(text, label):
    if not text or len(text) < 5:
        return text
    
    prompt = f"""
You are a professional resume writer with 10+ years experience.
Rewrite this resume {label} section to sound 100% like a real human wrote it.
Use natural language, vary sentence length, add subtle personal tone if appropriate.
Avoid robotic repetition, lists that are too perfect, over-formal phrasing.
Keep it concise, professional, ATS-friendly.
Original text:
{text}

Rewritten version (plain text only):
"""
    return query_ai(prompt, temperature=0.8)  # Higher temp = more human variation

# Generate from prompt (use Groq for better quality)
def generate_from_prompt(user_prompt):
    gen_prompt = f"""
User wants a resume based on: "{user_prompt}"

Generate a realistic, complete resume in strict JSON format ONLY. No extra text.
Keys must be exactly:
{{
  "name": "Full name (invent realistic if missing)",
  "job": "Job title",
  "email": "professional email",
  "phone": "phone with country code",
  "loc": "City, Country",
  "sum": "Professional summary (200-350 words, human-written style)",
  "edu": "Education section (formatted paragraphs or bullets)",
  "exp": "Work experience (3-6 realistic entries, detailed achievements)",
  "skills": "Skills (comma separated or short bullets)"
}}

Make it sound completely human-written: varied phrasing, some contractions, realistic details.
Output ONLY valid JSON.
"""
    raw = query_ai(gen_prompt, temperature=0.7, max_tokens=1800)
    try:
        data = json.loads(raw)
        # Extra humanization step
        for k in ['sum', 'exp', 'edu', 'skills']:
            if k in data:
                data[k] = humanize_text(data[k], k.replace('_', ' '))
        return data
    except:
        st.error("AI JSON generation failed. Try again or manual input.")
        return {}
