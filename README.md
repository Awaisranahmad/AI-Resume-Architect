# 📄 AI Resume Architect - Intelligent Resume Builder & Optimizer

**Craft ATS-Optimized, Professional Resumes with AI Assistance**

AI Resume Architect is an intelligent resume building and optimization platform that leverages advanced AI to help job seekers create compelling, ATS-compliant resumes. It provides real-time suggestions for content improvement, format optimization, and keyword alignment—ensuring your resume gets noticed by both AI systems and hiring managers.

---

## ✨ Features

- 🤖 **AI-Powered Resume Generation** – Generate professional resume content from job descriptions and experience
- ✍️ **Smart Content Suggestions** – Improve bullet points, descriptions, and achievements
- 📋 **ATS Optimization** – Ensure your resume passes Applicant Tracking Systems
- 🎯 **Keyword Alignment** – Match resume keywords with job descriptions
- 📊 **Resume Score Analysis** – Get detailed feedback on resume quality and completeness
- 🎨 **Professional Templates** – Choose from multiple ATS-friendly designs
- 💼 **Job Description Analysis** – Extract key requirements from job postings
- 🔄 **Version Control** – Save and manage multiple resume versions
- 📤 **Multiple Export Formats** – Download as PDF, DOCX, or plain text
- 💬 **Interactive AI Chat** – Ask for resume improvement suggestions
- 🌐 **Multi-Language Support** – Create resumes in different languages
- 📱 **Responsive Design** – Works seamlessly on desktop and mobile

---

## 🎯 Use Cases

- **Job Seekers** – Build a professional resume from scratch
- **Career Changers** – Reframe experience for new industries
- **Entry-Level Professionals** – Create impactful first resumes
- **Experienced Professionals** – Highlight achievements and leadership
- **International Candidates** – Localize resumes for different markets
- **Freelancers** – Create portfolios highlighting skills and projects

---

## 🛠️ Tech Stack

- **Language** – Python 3.10+
- **UI Framework** – Streamlit
- **LLM Engine** – Groq (Llama 3.3 70B, Llama 3 70B)
- **Orchestration** – LangChain
- **PDF Generation** – ReportLab / PyPDF2
- **Document Processing** – python-docx
- **Storage** – Session-based (in-memory)

---

## 📦 Requirements

- Python 3.10 or higher
- Groq API key ([Get one for free](https://console.groq.com/))
- Modern web browser

### Required Python Packages

```
streamlit
langchain-groq
langchain-core
python-docx
reportlab
pypdf2
python-dotenv
requests
```

Install dependencies:

```bash
pip install streamlit langchain-groq langchain-core python-docx reportlab pypdf2 python-dotenv requests
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Awaisranahmad/AI-Resume-Architect.git
cd AI-Resume-Architect
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Or set an environment variable:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### 4. Run the Application

```bash
streamlit run app.py
```

### 5. Access the Application

Open your browser and navigate to:

```
http://localhost:8501
```

---

## 💡 Usage Workflow

### Step 1: Create Profile
- Enter personal information (name, email, phone, location)
- Add professional summary or objective
- Specify target job title/industry

### Step 2: Add Experience
- Input job titles, companies, dates
- Add 3-5 achievement-focused bullet points
- AI suggests improvements based on industry standards

### Step 3: Add Education & Skills
- List degrees, certifications, and licenses
- Add technical and soft skills
- AI identifies missing skills based on target role

### Step 4: Optimize for Job
- Paste a job description
- AI highlights matching keywords
- Suggests additional skills or experience to emphasize

### Step 5: Review & Export
- Preview resume with multiple templates
- Check ATS compatibility score
- Download in preferred format (PDF, DOCX, TXT)

---

## 🎨 Features in Detail

### ATS Optimization
- Removes graphics and complex formatting
- Ensures proper keyword placement
- Validates section structure
- Checks readability metrics

### Resume Scoring
- **Content Completeness** – 0-100%
- **ATS Compatibility** – 0-100%
- **Keyword Match** – Shows matched/missed keywords
- **Readability Score** – Based on length, clarity, action verbs

### Smart Suggestions
- Replaces weak verbs with power action words
- Quantifies achievements where possible
- Identifies and fixes common resume mistakes
- Suggests industry-specific keywords

### Template Styles
- Modern Professional
- Classic Executive
- Creative Bold
- Minimalist Clean
- Corporate Standard

---

## 📂 Project Structure

```
AI-Resume-Architect/
├── app.py                      # Main Streamlit application
├── modules/
│   ├── resume_generator.py     # Resume content generation
│   ├── ats_optimizer.py        # ATS optimization engine
│   ├── keyword_matcher.py      # Job-resume keyword matching
│   ├── resume_scorer.py        # Resume quality scoring
│   └── suggestion_engine.py    # Content improvement suggestions
├── templates/
│   ├── templates.py            # Resume template definitions
│   ├── styles.css              # Template styling
│   └── prompts.py              # LLM prompt templates
├── utils/
│   ├── export.py               # PDF/DOCX export functions
│   ├── formatting.py           # Text formatting utilities
│   └── validators.py           # Input validation
├── data/
│   ├── power_verbs.json        # Action verb database
│   └── keywords.json           # Industry keywords
├── requirements.txt            # Python dependencies
└── .streamlit/
    └── secrets.toml            # API keys (not in version control)
```

---

## 🔍 ATS Optimization Details

The application automatically:
- ✅ Removes all images and graphics
- ✅ Uses standard fonts and formatting
- ✅ Organizes content in logical sections
- ✅ Extracts keywords from job descriptions
- ✅ Identifies skill gaps
- ✅ Validates date formats
- ✅ Checks for consistency
- ✅ Suggests keyword placement

---

## 📊 Resume Scoring Metrics

| Metric | Weight | Description |
|--------|--------|-------------|
| Completeness | 25% | All required sections present |
| Keyword Match | 25% | Alignment with target role |
| ATS Compatibility | 25% | Formatting and structure |
| Readability | 15% | Clarity and professionalism |
| Content Quality | 10% | Strength of bullet points |

---

## 🔒 Security & Privacy

- **Data Privacy** – Resumes are not stored or analyzed for training
- **API Security** – API keys never logged or exposed
- **Session-Based** – All data cleared after session ends
- **No Tracking** – No user data collected or shared
- **Secure Export** – Downloads use secure protocols

---

## ⚠️ Important Notes

- **Review Content** – AI suggestions should be reviewed for accuracy
- **Customization** – Tailor suggestions to your specific experience
- **Testing** – Test exported files on ATS systems before submitting
- **Privacy** – Don't include sensitive information during creation
- **Compliance** – Ensure resume complies with job application requirements

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 📞 Support & Feedback

For issues, questions, or suggestions:

- 🐛 **GitHub Issues**: [Report issues](https://github.com/Awaisranahmad/AI-Resume-Architect/issues)
- 💬 **Discussions**: [Start a discussion](https://github.com/Awaisranahmad/AI-Resume-Architect/discussions)
- 📧 **Email**: [Your contact email]

---

## 🙏 Acknowledgements

- [Groq](https://groq.com/) for powerful AI inference
- [Streamlit](https://streamlit.io/) for the web framework
- [LangChain](https://www.langchain.com/) for LLM orchestration
- Career coaches and HR professionals for domain expertise

---

## 🚀 Roadmap

- [ ] LinkedIn profile import
- [ ] Cover letter generation
- [ ] Interview preparation module
- [ ] Job application tracking
- [ ] Portfolio integration
- [ ] Team collaboration features
- [ ] Resume analytics dashboard

---

## 💡 Pro Tips

1. **Use Real Data** – AI works better with actual experience details
2. **Quantify Achievements** – Numbers make stronger impact
3. **Customize for Roles** – Adjust emphasis based on target position
4. **Update Regularly** – Refresh resume as skills and experience evolve
5. **Test Multiple Formats** – Try different templates for different industries

---

**Made with 💼 to help careers take flight**

*Your dream job starts with a great resume.*
